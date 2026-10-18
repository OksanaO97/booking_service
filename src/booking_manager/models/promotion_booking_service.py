from django.db import models
from core.models import BaseModel

class PromotionBookingService(BaseModel):
    promotion = models.ForeignKey(to='Promotion', on_delete=models.CASCADE, verbose_name='акция')
    booking_service = models.ForeignKey(to='BookingService', on_delete=models.CASCADE, verbose_name='услуга')
    discount_percent = models.PositiveSmallIntegerField(verbose_name='размер скидки в процентах', null=True, blank=True)

    class Meta:
        db_table = 'promotion_booking_service'
        verbose_name = 'услуга в акции'
        verbose_name_plural = 'услуги в акции'

    def __str__(self):
        return f"{self.promotion.name} в {self.booking_service.name} ({self.discount_percent})"