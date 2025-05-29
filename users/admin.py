from django.contrib import admin
from network.models import NetworkLink, Product

@admin.action(description='Очистить задолженность перед поставщиком')
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)

class NetworkLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country', 'city', 'supplier', 'debt', 'created_at')
    list_filter = ('city',)
    actions = [clear_debt]
    readonly_fields = ('created_at',)
    search_fields = ('name', 'city')

admin.site.register(NetworkLink, NetworkLinkAdmin)
admin.site.register(Product)