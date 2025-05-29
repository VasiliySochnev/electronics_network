from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    """CRUD-интерфейс для модели пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(is_active=True)
