from django.db import models
from core.models import BaseModel



class Promotion(BaseModel):

    name = models.CharField(
        max_length=50,
        verbose_name='название акции',
        unique=True
    )

    description = models.TextField(
        blank=True,
        verbose_name='описание акции'
    )


    start_date = models.DateField(
        verbose_name='дата начала действия',
        null=True,
        blank=True
    )

    end_date = models.DateField(
        verbose_name='дата окончания действия',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True,
        blank=True
    )

    booking_services = models.ManyToManyField(
        to='booking_manager.BookingService',
        verbose_name='услуги',
        related_name='promotions',
        through = 'PromotionBookingService'
        )


    class Meta:
        db_table = 'promotions'
        verbose_name = 'акция'
        verbose_name_plural = 'акции'
        ordering = ['-created_at', 'name']

    def __str__(self):
        return self.name

    #  1 акция распространяется на разные услуги, но и 1 услуга может быть в разных акциях