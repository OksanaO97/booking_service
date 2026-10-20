from django.db import models
from core.models import BaseModel
from booking_manager.models.managers.booking import BookingManager

class Booking(BaseModel):
    name = models.CharField(
        max_length=30,
        verbose_name='наименование',
        unique=True
    )
    is_active = models.BooleanField(
        verbose_name='активна',
        default=True,
        blank=True
    )
    visit_time = models.DateTimeField(
        verbose_name='время записи',
        null = True
    )


    booking_service = models.ForeignKey(
        to='BookingService',
        on_delete=models.SET_NULL,
        related_name='bookings',
        verbose_name='услуги',
        null=True,
    )

    barber = models.ForeignKey(to='account.Barber', related_name='bookings', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='барбер' )
    client = models.ForeignKey(to='account.Client', related_name='bookings', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='клиент')
    objects = BookingManager()


    class Meta:
        db_table = 'bookings'
        verbose_name = 'бронирование мастера'
        verbose_name_plural = 'бронирвоания мастеров'
        ordering = ['-created_at', 'name']

    def __str__(self):
        return self.name

# Связь «Один-ко-Многим». Один мастер (Barber) может иметь много записей на стрижку в таблице бронирований.
# Но у одного конкретного бронирования (в данную дату и время) может быть только один конкретный мастер.
# Теперь один клиент может приходить к нам в салон много раз (создавать много бронирований),
# но у каждого бронирования есть строго один владелец-клиент.