from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from network.models import NetworkLink, Product
from network.resources import NetworkLinkResource

from .models import User


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    """
    Админ-действие: сбросить задолженность перед поставщиком до 0
    для выбранных объектов NetworkLink.
    """
    queryset.update(debt=0)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Кастомизированная админка для модели User.
    Отображает ключевые поля и организует их в логические группы.
    """

    list_display = (
        "email",
        "first_name",
        "sur_name",
        "last_name",
        "phone",
        "city",
        "country",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_active", "country", "city")
    search_fields = ("email", "first_name", "last_name", "sur_name", "phone")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Личная информация",
            {
                "fields": (
                    "first_name",
                    "sur_name",
                    "last_name",
                    "phone",
                    "city",
                    "country",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


class NetworkLinkAdmin(ImportExportModelAdmin):
    """
    Админка для модели NetworkLink.
    Включает отображение уровня, ссылки на поставщика и фильтрацию по городу.
    """

    resource_class = NetworkLinkResource
    list_display = (
        "id",
        "name",
        "email",
        "country",
        "city",
        "supplier_link",  # Ссылка на поставщика
        "debt",
        "level",  # Уровень звена
        "created_at",
    )
    list_filter = ("city",)
    actions = [clear_debt]
    readonly_fields = ("created_at",)
    search_fields = ("name", "city")

    def supplier_link(self, obj):
        """
        Возвращает HTML-ссылку на поставщика в админке.
        """
        if obj.supplier:
            url = reverse("admin:network_networklink_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    def level(self, obj):
        """
        Возвращает уровень текущего звена сети.
        """
        return obj.level

    level.short_description = "Уровень звена"


# Регистрация моделей в админке
admin.site.register(NetworkLink, NetworkLinkAdmin)
admin.site.register(Product)
