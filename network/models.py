from django.db import models
from django.utils import timezone

from .utils import calculate_level


class Product(models.Model):
    """Модель товара, представляющая конкретный товар с характеристиками."""

    name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Название товара"
    )
    model = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Модель товара"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Цена товара",
    )
    description = models.TextField(
        max_length=300, blank=True, null=True, verbose_name="Описание товара"
    )
    release_date = models.DateField(blank=True, null=True, verbose_name="Дата релиза")
    amount_link = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Количество у поставщика"
    )
    network_link = models.ForeignKey(
        "NetworkLink", on_delete=models.CASCADE, verbose_name="Поставщик"
    )

    def __str__(self):
        """Строковое представление товара: название и модель."""
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]


class NetworkLink(models.Model):
    """Модель сетевого звена, представляющая поставщика или посредника в сети."""

    name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Название"
    )
    email = models.EmailField()
    country = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Страна"
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    street = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Улица"
    )
    house_number = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Номер строения"
    )
    products = models.ManyToManyField(
        "Product", through="NetworkProduct", blank=True, verbose_name="Товары"
    )
    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="поставщик",  # Обратная связь на поставщика
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
        verbose_name="Долг перед поставщиком",
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )

    @property
    def level(self):
        """
        Вычисляет уровень сетевого звена в иерархии поставщиков с помощью вспомогательной функции.
        """
        return calculate_level(self)

    def __str__(self):
        """Строковое представление: имя сетевого звена."""
        return self.name

    class Meta:
        verbose_name = "Сетевое звено"
        verbose_name_plural = "Сетевые звенья"
        ordering = ["name"]


class NetworkProduct(models.Model):
    """
    Промежуточная модель для связи товаров с сетевыми звеньями.
    Хранит количество товара у конкретного сетевого звена.
    """

    network_link = models.ForeignKey(
        "NetworkLink",
        on_delete=models.CASCADE,
        related_name="network_link_products",
        verbose_name="Сетевое звено",
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        """Строковое представление: количество товара и имя сетевого звена."""
        return f"{self.quantity} x {self.product.name} в сетевом звене {self.network_link.name}"
