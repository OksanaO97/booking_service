from django.db.models.signals import post_save
from django.dispatch import receiver
from booking_manager.models import Booking
from django.db.models import Count





@receiver(post_save, sender=Booking)
def signal_post_save_client_with_booking_1(sender, instance, created,**kwargs):
    if not instance.client:
        return

    my_bookings = Booking.objects.filter(client=instance.client, is_active=False).aggregate(books=Count('id'))
    books_count = my_bookings['books']
    if books_count <= 2:
        instance.client.status = 'NOOB'
    elif 3 <= books_count <= 9:
        instance.client.status= 'REGULAR'
    elif books_count >= 10:
        instance.client.status = 'VIP'

    instance.client.save()


    # Сигнал, который автоматически изменяет статус клиента в зависимости от количества его активных
    # бронирований(тех которые уже завершились). При 0–2 бронированиях клиент получает статус NOOB, при 3–9 — REGULAR, при 10 и более — VIP.