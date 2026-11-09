from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from account.managers import UserManager
from core.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=64, null=True, blank=True, unique=True, verbose_name='имя пользователя')
    phone = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='телефон')
    first_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='имя')
    last_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='фамилия')
    is_staff = models.BooleanField(default=False, verbose_name='статус персонала')
    email = models.EmailField(max_length=64, unique=True, verbose_name='электронная почта')
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        ordering = ["-id","-created_at"]
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'




