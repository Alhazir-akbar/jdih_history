from django.urls import path, include
from rest_framework import routers
from peraturan import views

router = routers.DefaultRouter()

# Di sini kita akan mendaftarkan viewset nanti, misalnya:
# router.register(r'peraturan', views.PeraturanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
