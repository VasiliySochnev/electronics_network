from django.db import models


class Product(models.Model):
    """Модель товара."""

    name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Название товара"
    )
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name="Модель товара")
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
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]


class NetworkLink(models.Model):
    """Модель сетевого звена."""

    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название")
    email = models.EmailField()
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    street = models.CharField(max_length=100, blank=True, null=True, verbose_name="Улица")
    house_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Номер строения")
    products = models.ManyToManyField(
        "Product", through="NetworkProduct", verbose_name="Товары"
    )
    supplier = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='поставщик'
    )
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Задолжность перед поставщиком")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сетевое звено"
        verbose_name_plural = "Сетевые звенья"
        ordering = ["name"]


class NetworkProduct(models.Model):
    """Промежуточная модель для хранения количества каждого товара в сетевом звене."""

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
        return f"{self.quantity} x {self.product.name} в сетевом звене {self.network_link.pk}"