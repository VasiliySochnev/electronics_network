from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    Обеспечивает создание пользователя с безопасной обработкой пароля.
    Пароль скрыт в ответах API.
    """

    class Meta:
        model = User
        fields = "__all__"  # Включаем все поля модели User
        extra_kwargs = {
            "password": {"write_only": True}  # Пароль не отображается в сериализованных ответах
        }

    def create(self, validated_data):
        """
        Переопределённый метод создания пользователя:
        - Извлекает и хеширует пароль перед сохранением.
        - Создаёт экземпляр пользователя с использованием validated_data.
        """
        password = validated_data.pop("password", None)  # Удаляем пароль из словаря validated_data
        user = User(**validated_data)  # Создаём пользователя без пароля

        if password:
            user.set_password(password)  # Хешируем пароль безопасно
        user.save()
        return user
