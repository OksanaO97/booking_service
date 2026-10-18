import datetime
from django.db import models
from core.models import BaseModel


class Barbershop(BaseModel):
    name = models.CharField(
        max_length=50,
        verbose_name='название',
        unique=True
    )

    address = models.CharField(
        max_length=50,
        verbose_name='адрес',
    )

    phone = models.CharField(
        max_length=50,
        verbose_name='телефон',
        blank=True
    )

    description = models.TextField(
        blank=True,
        verbose_name='описание'
    )

    opening_time = models.TimeField(
        default=datetime.time(9,0),
        verbose_name='время открытия'
    )

    closing_time = models.TimeField(
        default=datetime.time(21,0),
        verbose_name='время закрытия'
    )

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True,
        blank=True
    )

    class Meta:
        db_table = 'barbershops'
        verbose_name = 'филиал'
        verbose_name_plural = 'филиалы'
        ordering = ['-created_at', 'name']

    def __str__(self):
        return self.name


#  один филиал имеет много мастеров, но один мастер работает в одном конкретном филиале.
#  1 товар может быть в разных филлиалах, и в 1 филлиале м.б. много товаров
#  1 конкретное бронирование относится к 1 конкретному филлиалу, но в 1 филлиале может быть много бронирований