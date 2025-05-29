from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkLinkViewSet

router = DefaultRouter()
router.register(r'network', NetworkLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
