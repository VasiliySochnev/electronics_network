from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import NetworkLink


class NetworkLinkResource(resources.ModelResource):
    """
    Ресурс для импорта/экспорта модели NetworkLink через Django Import-Export.

    Обеспечивает возможность работы с данными в формате Excel/CSV, включая
    связи между объектами (в частности, поле 'supplier' — внешний ключ на другое звено сети).
    """

    # Настройка поля supplier (внешний ключ) для корректной работы импорта/экспорта
    supplier = fields.Field(
        column_name="supplier",  # Название столбца в Excel-файле
        attribute="supplier",  # Атрибут модели, соответствующий полю supplier
        widget=ForeignKeyWidget(
            NetworkLink, "id"
        ),  # Использует внешний ключ по полю id
    )

    class Meta:
        model = NetworkLink  # Указываем модель, с которой работает ресурс

        # Явно перечисляем поля, которые должны участвовать в импорте/экспорте
        fields = (
            "id",  # Уникальный идентификатор звена
            "name",  # Название звена сети
            "email",  # Контактный email
            "country",  # Страна
            "city",  # Город
            "street",  # Улица
            "house_number",  # Номер дома
            "supplier",  # Внешний ключ на поставщика
            "debt",  # Задолженность перед поставщиком
        )
