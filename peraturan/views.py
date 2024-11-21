from rest_framework import viewsets, status
from rest_framework.response import Response

from peraturan.authentication import SessionJWTAuthentication
from peraturan.utils.utils import extract_pdf_content
from .models import Peraturan, PeraturanVersion
from .serializers import PeraturanSerializer, PeraturanVersionSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect

class PeraturanViewSet(viewsets.ModelViewSet):
    queryset = Peraturan.objects.all()
    serializer_class = PeraturanSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def add_version(self, request, pk=None):
        peraturan = self.get_object()
        serializer = PeraturanVersionSerializer(data=request.data)
        if serializer.is_valid():
            # Set version number
            last_version = peraturan.versions.last()
            if last_version:
                version_number = last_version.version_number + 1
            else:
                version_number = 1
            serializer.save(peraturan=peraturan, version_number=version_number, updated_by=request.user)
            # TODO: Add logic for PDF extraction and field change detection
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PeraturanVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PeraturanVersion.objects.all()
    serializer_class = PeraturanVersionSerializer
    permission_classes = [IsAuthenticated]

    def save(self, *args, **kwargs):
        # Ekstraksi PDF
        if self.pdf_file:
            self.pdf_file.seek(0)
            extracted_text = extract_pdf_content(self.pdf_file)
            print('extracted_text: ', extracted_text)
            self.extracted_content = {'text': extracted_text}
        super().save(*args, **kwargs)

        # Pelacakan perubahan
        previous_version = PeraturanVersion.objects.filter(
            peraturan=self.peraturan,
            version_number=self.version_number - 1
        ).first()
        if previous_version:
            changed_fields = {}
            # Bandingkan field Peraturan
            peraturan_fields = [f.name for f in Peraturan._meta.fields if f.name not in ('id', 'created_at', 'updated_at')]
            for field in peraturan_fields:
                old_value = getattr(previous_version.peraturan, field)
                new_value = getattr(self.peraturan, field)
                if old_value != new_value:
                    changed_fields[field] = {'old': old_value, 'new': new_value}
            # Bandingkan isi PDF
            if previous_version.extracted_content != self.extracted_content:
                changed_fields['extracted_content'] = 'Content changed.'
            self.changed_fields = changed_fields
        self.save(update_fields=['changed_fields'])
