from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import NetworkLinkViewSet


router = DefaultRouter()
router.register('network', NetworkLinkViewSet, basename='network_link')

urlpatterns = [
    path("", include(router.urls)),
]
