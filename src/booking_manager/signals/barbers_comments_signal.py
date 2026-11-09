from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from booking_manager.models import Comment
from django.db.models import Avg




@receiver([post_save, post_delete], sender=Comment)
def signal_post_save_delete_comment_with_rating_1(sender, instance, **kwargs):
    if not instance.barber:
        return

    barber = instance.barber
    new_rating = Comment.objects.filter(barber=barber, is_published=True).aggregate(Avg('rating'))['rating__avg']
    barber.rating = new_rating or 0.0
    barber.save()


    # Сигнал, который автоматически пересчитывают поле Barber.rating при создании, изменении или удалении комментария.
    # В расчёте участвуют только опубликованные комментарии. Если опубликованных комментариев нет, рейтинг должен принимать значение None.