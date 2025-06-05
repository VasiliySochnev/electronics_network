from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """
    Пользовательское разрешение, разрешающее доступ только активным сотрудникам.

    Условия доступа:
    - Пользователь должен быть аутентифицирован
    - Пользователь должен иметь флаг `is_staff=True`
    - Пользователь должен быть активен (`is_active=True`)
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь доступ к представлению.

        :param request: объект запроса
        :param view: объект представления
        :return: True, если пользователь соответствует условиям, иначе False
        """
        return (
            request.user
            and request.user.is_authenticated  # Пользователь должен быть авторизован
            and request.user.is_staff  # Должен быть сотрудником (staff)
            and request.user.is_active  # Должен быть активен
        )
