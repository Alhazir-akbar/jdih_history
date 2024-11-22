# jdih_history/base_viewset.py

from rest_framework import viewsets, status
from .exception_handler import api_response

class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet yang mengoverride metode standar DRF untuk menggunakan
    format respons yang konsisten.
    """

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(
            success=True,
            message="Data berhasil diambil",
            data=response.data,
            status_code=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return api_response(
            success=True,
            message="Data berhasil diambil",
            data=response.data,
            status_code=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(
            success=True,
            message="Data berhasil dibuat",
            data=response.data,
            status_code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(
            success=True,
            message="Data berhasil diperbarui",
            data=response.data,
            status_code=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return api_response(
            success=True,
            message="Data berhasil diperbarui",
            data=response.data,
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return api_response(
            success=True,
            message="Data berhasil dihapus",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
