from django.db import transaction
from django.core.exceptions import ValidationError
from account.models import Barber
from datetime import timedelta
from booking_manager.models import Booking

def create_booking_transaction(booking, barber):
    with transaction.atomic():
       our_booking = Booking.objects.get(id=booking.id)
       our_barber = Barber.objects.select_for_update(nowait=True).get(id=barber.id)
       time_to_visit  = our_booking.visit_time
       duration = our_booking.booking_service.duration_minute
       time_to_finish = time_to_visit + timedelta(minutes=duration)

       close_bookings = Booking.objects.filter(barber=our_barber, is_active=True, visit_time__lt=time_to_finish)

       for other_book in close_bookings:
           if other_book.id == booking.id:
                continue

           other_book_finish = other_book.visit_time + timedelta(minutes=other_book.booking_service.duration_minute)

           if other_book_finish > time_to_visit:
               raise ValidationError(
                   {"barber": f"Barber '{barber.user.first_name}' is busy! Overlap detected with booking #{other_book.id}."}
               )

    return booking


# Функция создания бронирования, которая предотвращает одновременную запись двух клиентов к одному барберу на пересекающееся время.
# При обнаружении пересечения отменяется создание новой записи.
