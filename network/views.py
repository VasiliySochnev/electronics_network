from rest_framework import viewsets
from .models import NetworkLink
from .serializers import NetworkLinkSerializer, NetworkLinkDetailSerializer
from users.permissions import IsActiveStaff
from .filters import NetworkLinkFilter
from django_filters.rest_framework import DjangoFilterBackend

class NetworkLinkViewSet(viewsets.ModelViewSet):
    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkLinkFilter

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return NetworkLinkDetailSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        # Удалить поле `debt` перед обновлением, если оно было передано
        request.data.pop('debt', None)
        return super().update(request, *args, **kwargs)

