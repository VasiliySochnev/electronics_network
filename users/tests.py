from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from rest_framework import status


class UserAPITestCase(TestCase):
    """
    Набор тестов для проверки API, связанного с моделью пользователя.
    """

    def setUp(self):
        """
        Подготовка тестовых данных: создаётся клиент и тестовый пользователь.
        """
        self.client = APIClient()

        # Данные для создания нового пользователя через API
        self.new_user_data = {
            'email': 'newuser@mail.ru',
            'password': 'strongpassword123',
            'first_name': 'Иван',
            'last_name': 'Петров'
        }

        # Существующий пользователь для аутентификации
        self.existing_user = User.objects.create_user(
            email='existinguser@mail.ru',
            password='password123',
            is_staff=False,
            is_active=True
        )

    def test_user_creation_password_hashed(self):
        """
        Проверяет, что при создании пользователя пароль сохраняется в захешированном виде.
        """
        url = reverse('user-list')
        response = self.client.post(url, self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Получаем пользователя из базы и проверяем, что пароль захеширован
        created_user = User.objects.get(email=self.new_user_data['email'])
        self.assertNotEqual(created_user.password, self.new_user_data['password'])
        self.assertTrue(created_user.check_password(self.new_user_data['password']))

    def test_user_list_requires_authentication(self):
        """
        Проверяет, что список пользователей недоступен без авторизации.
        """
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])

    def test_authenticated_user_can_access_list(self):
        """
        Проверяет, что авторизованный пользователь может получить список пользователей.
        """
        self.client.force_authenticate(user=self.existing_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
