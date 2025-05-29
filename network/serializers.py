from rest_framework import serializers
from .models import NetworkLink, Product, NetworkProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class NetworkLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkLink
        exclude = ('debt',)  # запрещено обновление через API

class NetworkLinkDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.StringRelatedField()

    class Meta:
        model = NetworkLink
        fields = '__all__'


class NetworkProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkProduct
        fields = '__all__'