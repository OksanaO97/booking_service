from django.db import models
from django.core.validators import MinValueValidator
from src.booking_manager.constants import CategoryChoices

class Booking(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='наименование',
        unique=True
    )
    description = models.TextField(
        max_length=255,
        verbose_name='описание',
        null=True,
        blank=True
    )
    price = models.FloatField(
        verbose_name='цена',
        validators=[MinValueValidator(0)]
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices,
        verbose_name='категория',
        default=CategoryChoices.HAIRCUT
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'booking'
        verbose_name = 'бронирование мастера'
        ordering = ['-created_at', '-price', 'category']

    def __str__(self):
        return self.name