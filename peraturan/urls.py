from django.urls import path, include
from rest_framework import routers
from .views import PeraturanViewSet, PeraturanVersionViewSet

router = routers.DefaultRouter()
router.register(r'peraturan', PeraturanViewSet)
router.register(r'versions', PeraturanVersionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
