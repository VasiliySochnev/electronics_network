from django_filters import rest_framework as filters

from .models import NetworkLink


class NetworkLinkFilter(filters.FilterSet):
    """
    Фильтр для модели NetworkLink, используемый в DRF вьюсетах
    для фильтрации по стране и городу.
    """

    # Фильтрация по точному совпадению названия страны (без учета регистра).
    country = filters.CharFilter(field_name="country", lookup_expr="iexact")

    # Фильтрация по городу с частичным совпадением (без учета регистра).
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")

    class Meta:
        model = NetworkLink
        fields = ["country"]
