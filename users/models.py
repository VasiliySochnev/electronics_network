from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Модель пользователя."""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(
        max_length=50, verbose_name="Имя", blank=True, null=True
    )
    sur_name = models.CharField(
        max_length=50, verbose_name="Отчество", blank=True, null=True
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", blank=True, null=True
    )
    phone = models.CharField(
        max_length=35, verbose_name="телефон", blank=True, null=True
    )
    city = models.CharField(
        max_length=100, verbose_name="город", blank=True, null=True
    )
    country = models.CharField(
        max_length=100, verbose_name="страна", blank=True, null=True
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Активность", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        full_name = f"{self.last_name or ''} {self.first_name or ''} {self.sur_name or ''}".strip()
        return full_name if full_name else self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

