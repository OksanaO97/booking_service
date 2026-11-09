from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from account.models import Client
from django.core.cache import cache




@receiver([post_save, post_delete], sender=Client)
def client_post_save_delete_cache_signal(sender, instance, **kwargs):
    cache_key = 'active_client_profile_list' + str(instance.user.id)
    cache.delete(cache_key)


    # Сигнал, который при изменении информации о клиенте сбрасывает кэш.
    # для клиента: cache_key = 'active_client_profile_list' + str(instance.id)