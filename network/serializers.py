from rest_framework import serializers
from .models import NetworkLink, NetworkProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    Используется для отображения всех полей продукта.
    """

    class Meta:
        model = Product
        fields = "__all__"  # Включаем все поля модели Product


class NetworkLinkSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkLink.
    Добавляет вычисляемое поле 'level' и исключает поле 'debt',
    так как его нельзя обновлять через API.
    """
    level = serializers.SerializerMethodField()  # Вычисляемое поле, не связанное напрямую с моделью

    class Meta:
        model = NetworkLink
        exclude = ("debt",)  # debt исключается из сериализации

    def get_level(self, obj):
        """
        Метод для получения значения поля 'level'.
        """
        return obj.level


class NetworkProductInlineSerializer(serializers.ModelSerializer):
    """
    Вложенный сериализатор для модели NetworkProduct.
    Отображает продукт и его количество.
    Используется в детализации NetworkLink.
    """
    product = ProductSerializer()  # Вложенный сериализатор для отображения данных продукта

    class Meta:
        model = NetworkProduct
        fields = ["product", "quantity"]  # Только необходимые поля


class NetworkLinkDetailSerializer(serializers.ModelSerializer):
    """
    Детализированный сериализатор для модели NetworkLink.
    Отображает поставщика (в текстовом виде) и связанные продукты.
    """
    supplier = serializers.StringRelatedField()  # Используется строковое представление связанного объекта
    products = NetworkProductInlineSerializer(
        source="network_link_products",  # Связь с NetworkProduct по related_name
        many=True,
        read_only=True
    )

    class Meta:
        model = NetworkLink
        fields = "__all__"  # Отображаем все поля, кроме исключённого ранее 'debt'


class NetworkProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkProduct.
    Используется для создания и обновления связей между сетью и продуктами.
    """

    class Meta:
        model = NetworkProduct
        fields = "__all__"  # Включаем все поля
