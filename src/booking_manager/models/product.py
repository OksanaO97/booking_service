from django.db import models
from core.models import BaseModel



class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.PositiveIntegerField(verbose_name='цена за штуку')
    amount = models.PositiveIntegerField(verbose_name='количество на складе')


    bookings = models.ManyToManyField(
        to='Booking',
        verbose_name='бронирования',
        related_name='products',
        through='ProductBooking'
    )

    class Meta:
        db_table = 'products'
        verbose_name = 'товар'
        ordering = ['-created_at', '-price', '-amount']
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name



# Один товар может быть добавлен в разные бронирования, и в то же время внутри одного бронирования клиент может купить сразу несколько разных товаров
# Связь многие ко многим