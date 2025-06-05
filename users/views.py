from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.

    Предоставляет стандартные CRUD-операции:
    - Создание (доступно без аутентификации)
    - Просмотр, обновление и удаление (только для аутентифицированных)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений в зависимости от действия.

        - Для создания (`create`) — доступ разрешён всем (AllowAny)
        - Для остальных действий — требуется аутентификация (IsAuthenticated)
        """
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Выполняется при создании пользователя через API.

        Принудительно устанавливает `is_active=True` для новых пользователей.
        """
        serializer.save(is_active=True)
