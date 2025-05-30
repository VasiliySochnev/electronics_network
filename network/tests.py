from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from network.models import NetworkLink
from users.models import User
from rest_framework import status

class NetworkLinkAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создание пользователей
        self.staff_user = User.objects.create_user(
            email='staff@mail.ru',
            password='password123',
            is_staff=True,
            is_active=True
        )
        self.normal_user = User.objects.create_user(
            email='user@mail.ru',
            password='password123',
            is_staff=False,
            is_active=True
        )

        # Два объекта сети с разными странами
        self.link_ru = NetworkLink.objects.create(
            name="RU Supplier", email="ru@mail.ru", country="Russia", city="Moscow", debt=100.0
        )
        self.link_us = NetworkLink.objects.create(
            name="US Supplier", email="us@mail.com", country="USA", city="New York", debt=200.0
        )

    def test_filter_by_country(self):
        """Проверка фильтрации по полю country."""
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.get(reverse('network_link-list'), {'country': 'Russia'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['country'], 'Russia')

    def test_unauthenticated_access_denied(self):
        """Неавторизованный пользователь не должен получить доступ."""
        response = self.client.get(reverse('network_link-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_access_denied(self):
        """Пользователь без is_staff не должен получить доступ."""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(reverse('network_link-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_access_allowed(self):
        """Пользователь is_staff и is_active имеет доступ."""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(reverse('network_link-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_network_link_without_modifying_debt(self):
        """Обновление звена через PATCH не меняет поле debt."""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('network_link-detail', args=[self.link_ru.id])
        payload = {
            'name': 'Updated RU Supplier',
            'city': 'Saint Petersburg',
            'debt': 0  # Попытка изменить поле debt, должно игнорироваться
        }
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.link_ru.refresh_from_db()
        self.assertEqual(self.link_ru.name, 'Updated RU Supplier')
        self.assertEqual(self.link_ru.city, 'Saint Petersburg')
        self.assertEqual(float(self.link_ru.debt), 100.0)

    def test_put_does_not_update_debt(self):
        """Обновление звена через PUT не меняет поле debt."""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('network_link-detail', args=[self.link_ru.id])
        payload = {
            "name": "PUT Updated RU Supplier",
            "email": "ru@mail.ru",
            "country": "Russia",
            "city": "Kazan",
            "street": "Pushkina",
            "house_number": "10",
            "debt": 0  # Попытка изменить debt
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.link_ru.refresh_from_db()
        self.assertEqual(self.link_ru.name, "PUT Updated RU Supplier")
        self.assertEqual(self.link_ru.city, "Kazan")
        self.assertEqual(float(self.link_ru.debt), 100.0)
