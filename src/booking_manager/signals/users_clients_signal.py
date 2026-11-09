from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import User, Client, Barber




@receiver(post_save, sender=User)
def signal_post_save_user_with_client_1(sender, instance, created,**kwargs):


    if created:
        if instance.is_staff:
            Barber.objects.get_or_create(user_id=instance.id)
        else:
            Client.objects.get_or_create(user_id=instance.id)


    # При создании нового пользователя автоматически создаётся связанный объект Client или Barber