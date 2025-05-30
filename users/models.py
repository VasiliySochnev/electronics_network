from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер модели пользователя с поддержкой создания пользователей по email."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с указанными email и паролем.
        """
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # хешируем пароль
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Создание обычного пользователя.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создание суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя, использующая email вместо username.
    """

    username = None  # Удаляем стандартное поле username
    email = models.EmailField(unique=True, verbose_name="Email")  # Основной идентификатор

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

    USERNAME_FIELD = "email"  # Используем email как логин
    REQUIRED_FIELDS = []  # Поля, обязательные при создании суперпользователя

    objects = UserManager()  # Подключаем кастомный менеджер

    def __str__(self):
        """
        Возвращает строковое представление пользователя.
        Предпочтительно — ФИО, иначе — email.
        """
        full_name = f"{self.last_name or ''} {self.first_name or ''} {self.sur_name or ''}".strip()
        return full_name if full_name else self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
