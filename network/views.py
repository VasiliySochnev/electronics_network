from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from users.permissions import IsActiveStaff
from .filters import NetworkLinkFilter
from .models import NetworkLink
from .serializers import NetworkLinkDetailSerializer, NetworkLinkSerializer


class NetworkLinkViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с объектами NetworkLink.

    Позволяет выполнять стандартные CRUD-операции:
    - Список всех связей сети
    - Получение детальной информации
    - Создание, обновление и удаление записей

    Применяются фильтры по стране и городу, а также ограничение доступа —
    только активные сотрудники (IsActiveStaff).
    """

    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkLinkFilter

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от действия.

        Для действия `retrieve` (детальный просмотр) используется
        расширенный сериализатор `NetworkLinkDetailSerializer`.
        Для остальных — базовый `NetworkLinkSerializer`.
        """
        if self.action == "retrieve":
            return NetworkLinkDetailSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        """
        Переопределяет метод обновления объекта.

        Удаляет поле `debt` из данных запроса, чтобы предотвратить
        его обновление через API, так как оно исключено в сериализаторе.
        """
        request.data.pop("debt", None)  # Исключаем поле из запроса
        return super().update(request, *args, **kwargs)
