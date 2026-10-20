from django.db import models
from core.models import BaseModel

class ProductBooking(BaseModel):
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, verbose_name='товар')
    booking = models.ForeignKey(to='Booking', on_delete=models.CASCADE, verbose_name='бронирование')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')
    total_price = models.FloatField(null=True, verbose_name='итоговая стоимость')


    class Meta:
        db_table = 'product_bookings'
        verbose_name = 'товар в бронировании'
        verbose_name_plural = 'товары в бронированиях'



