from django_filters import rest_framework as filters
from .models import NetworkLink

class NetworkLinkFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='country', lookup_expr='iexact')

    class Meta:
        model = NetworkLink
        fields = ['country']
