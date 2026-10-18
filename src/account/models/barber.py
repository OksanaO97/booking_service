from django.db import models

from core.models import BaseModel, RatingMixin


class Barber(BaseModel, RatingMixin):
    experience_year = models.IntegerField(verbose_name='опыт')
    user = models.OneToOneField(to='account.User', related_name='barber', on_delete=models.CASCADE, verbose_name='пользователь')
    barbershop = models.ForeignKey(to='booking_manager.Barbershop', related_name='barbers', on_delete=models.CASCADE, verbose_name='филиал')


    class Meta:
        ordering = ["-id","-created_at"]
        db_table = "barbers"
        verbose_name = "Барбер"
        verbose_name_plural = "Барберы"