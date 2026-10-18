from django.db import models
from core.models import BaseModel
from booking_manager.constants import CategoryChoices

class BookingService(BaseModel):
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices,
        verbose_name='категория',
        default=CategoryChoices.HAIRCUT
    )

    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.PositiveIntegerField(verbose_name='стоимость')
    duration_minute = models.PositiveIntegerField(verbose_name='продолжительность')
    is_active = models.BooleanField(default=True, verbose_name='активна')


    class Meta:
        db_table = 'booking_services'
        verbose_name = 'Услуга'
        ordering = ['-created_at', '-price', 'category']
        verbose_name_plural = 'услуги'

    def __str__(self):
        return self.name


# Одна услуга во многих записях (1 ко многим)