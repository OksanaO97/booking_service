
from django.db import models
from account.constants import ClientStatusChoices

from core.models import BaseModel


class Client(BaseModel):
    status = models.CharField(choices=ClientStatusChoices, default=ClientStatusChoices.NOOB, verbose_name='статус')
    date_of_birth = models.DateField(null=True, verbose_name='дата рождения', blank=True)
    user = models.OneToOneField(to='account.User', related_name='client', on_delete=models.CASCADE, verbose_name='пользователь')


    class Meta:
        ordering = ["-id","-created_at"]
        db_table = "clients"
        verbose_name = "Клиент"
        verbose_name_plural = 'Клиенты'