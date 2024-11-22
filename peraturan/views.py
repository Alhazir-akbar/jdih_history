# peraturan/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from jdih_history.base_viewset import BaseViewSet
from jdih_history.exception_handler import api_response
from peraturan.pagination import PeraturanVersionPagination


from .authentication import SessionJWTAuthentication
from .utils.utils import extract_pdf_content
from .models import Peraturan, PeraturanVersion
from .serializers import PeraturanSerializer, PeraturanVersionSerializer

class PeraturanViewSet(BaseViewSet):
    queryset = Peraturan.objects.all()
    serializer_class = PeraturanSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """
        Override the create method to automatically create the first version
        when a new Peraturan is created.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            peraturan = serializer.save()
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file:
                # Membuat versi pertama
                PeraturanVersion.objects.create(
                    peraturan=peraturan,
                    version_number=1,
                    pdf_file=pdf_file,
                    extracted_content=extract_pdf_content(pdf_file),
                    updated_by=request.user
                )
            else:
                return Response({"detail": "Lampiran PDF 'pdf_file' diperlukan saat membuat peraturan baru."}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def add_version(self, request, pk=None):
        """
        Custom action to add a new version to an existing Peraturan.
        """
        peraturan = self.get_object()
        serializer = PeraturanVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            last_version = peraturan.versions.last()
            version_number = last_version.version_number + 1 if last_version else 1
            pdf_file = request.FILES.get('pdf_file')

            if not pdf_file:
                return Response({"detail": "Lampiran PDF diperlukan untuk menambahkan versi baru."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                peraturan_version = PeraturanVersion.objects.create(
                    peraturan=peraturan,
                    version_number=version_number,
                    pdf_file=pdf_file,
                    extracted_content=extract_pdf_content(pdf_file),
                    updated_by=request.user
                )
            except Exception as e:
                return Response({"detail": f"Error processing PDF: {str(e)}"}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Logika perbandingan bisa ditambahkan di sini jika belum lengkap
        return Response(PeraturanVersionSerializer(peraturan_version).data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to automatically create a new version
        when the main Peraturan data is updated.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_data = {field.name: getattr(instance, field.name) for field in instance._meta.fields}

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Simpan data terbaru
            self.perform_update(serializer)

            # Bandingkan perubahan antara data lama dan baru
            new_data = serializer.validated_data
            changed_fields = {
                field: {'old': old_data[field], 'new': new_data.get(field, old_data[field])}
                for field in old_data.keys() if old_data[field] != new_data.get(field, old_data[field])
            }

            # Buat versi baru hanya jika ada perubahan
            if changed_fields:
                pdf_file = request.FILES.get('pdf_file')
                if not pdf_file:
                    return Response({"detail": "Lampiran PDF diperlukan untuk membuat versi baru."}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                
                PeraturanVersion.objects.create(
                    peraturan=instance,
                    version_number=instance.versions.count() + 1,
                    pdf_file=pdf_file,
                    extracted_content=extract_pdf_content(pdf_file),
                    changed_fields=changed_fields,
                    updated_by=request.user
                )

        return Response(serializer.data)

class PeraturanVersionViewSet(BaseViewSet):
    queryset = PeraturanVersion.objects.all()
    serializer_class = PeraturanVersionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PeraturanVersionPagination

    def get_annotated_queryset(self, peraturan_id=None):
        queryset = PeraturanVersion.objects.all()

        if peraturan_id:
            queryset = queryset.filter(peraturan_id=peraturan_id)
        
        return queryset.annotate(
            peraturan_name = Concat(
                F('peraturan__judul_peraturan'),
                Value(''),
                output_field=CharField()
            )
        ).values('id', 'version_number', 'peraturan_name', 'peraturan', 'is_final')

    @action(detail=False, methods=['get'])
    def list_versions_id(self, request):
        peraturan_id = request.query_params.get('id_peraturan')
        if not peraturan_id:
            return Response({"detail": "Parameter 'id_peraturan' diperlukan."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not peraturan_id.isdigit():
            return Response({"detail":"id_peraturan harus berupa angka."}, status=status.HTTP_400_BAD_REQUEST)
        
        query = self.get_annotated_queryset(peraturan_id=int(peraturan_id))
        return api_response(success=True, message="List version pada satu dokument.", data=list(query), status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_versions(self, request, *args, **kwargs):
        queryset = self.get_annotated_queryset()
        return Response(list(queryset), status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def compare(self, request):
        """
        Custom endpoint to compare two versions.
        Expected query parameters: version1 and version2
        """
        version1_id = request.query_params.get('version1')
        version2_id = request.query_params.get('version2')

        if not version1_id or not version2_id:
            return Response({"detail": "Parameter 'version1' dan 'version2' diperlukan."}, status=status.HTTP_400_BAD_REQUEST)
        
        version1 = get_object_or_404(PeraturanVersion, id=version1_id)
        version2 = get_object_or_404(PeraturanVersion, id=version2_id)

        # Pastikan kedua versi terkait dengan peraturan yang sama
        if version1.peraturan != version2.peraturan:
            return Response({"detail": "Kedua versi harus terkait dengan peraturan yang sama."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Menggabungkan perubahan dari kedua versi
        comparison = {}
        for field, changes in version2.changed_fields.items():
            comparison[field] = changes

        return Response({
            "peraturan": version1.peraturan.judul_peraturan,
            "version1": PeraturanVersionSerializer(version1).data,
            "version2": PeraturanVersionSerializer(version2).data,
            "comparison": comparison
        }, status=status.HTTP_200_OK)