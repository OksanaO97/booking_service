from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from booking_manager.models import BookingService
from django.core.cache import cache




@receiver([post_save, post_delete], sender=BookingService)
def booking_service_post_save_delete_cache_signal(sender, instance, **kwargs):
    cache_key = 'active_booking_services_list'
    cache.delete(cache_key)


    # Сигнал, который при создании, изменении или удалении услуги реализовывает инвалидацию кеша.