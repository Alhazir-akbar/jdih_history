# peraturan/urls.py

from django.urls import path, include
from rest_framework import routers
from .views import PeraturanViewSet, PeraturanVersionViewSet

router = routers.DefaultRouter()
router.register(r'peraturan', PeraturanViewSet, basename='peraturan')
router.register(r'versions', PeraturanVersionViewSet, basename='peraturanversion')

urlpatterns = [
    path('', include(router.urls)),
]
