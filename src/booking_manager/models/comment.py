from django.db import models
from core.models import BaseModel, RatingMixin



class Comment(BaseModel, RatingMixin):

    text = models.TextField(
        verbose_name='текст',
        blank=True
    )

    is_published = models.BooleanField(
        verbose_name='опубликован',
        default=True,
        blank=True
    )

    client = models.ForeignKey(
        to='account.Client',
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='клиент')

    barber = models.ForeignKey(
        to='account.Barber',
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='барбер')

    booking = models.OneToOneField(
        to='booking_manager.Booking',
        related_name='comment',
        on_delete=models.CASCADE,
        verbose_name='бронирование мастера')


    class Meta:
        db_table = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['-created_at', '-rating']

    def __str__(self):
        return self.text[:50] if self.text else f"Оценка: {self.rating}"

    #  1 клиент может оставлять много комментариев, но каждый комментарий пренадлежит толкьо одному клиенту
    # Об 1 барбере могут оставить много комментариев, нокаждый комментарий лишь об одном барбере
    # В каждом бронировании можно оставить лишь 1 комментарий