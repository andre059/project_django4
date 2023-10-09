from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class EmailVerificationToken(models.Model):
    """
    Модель предназначена для хранения информации о токене верификации электронной почты пользователя.
    Она связана с конкретным пользователем через внешний ключ user,
    хранит сам токен token и дату его создания created_at.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')

    token = models.CharField(max_length=255, unique=True, verbose_name='токен верификации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания токена')

    def __str__(self):
        return f'{self.token} {self.created_at}'
