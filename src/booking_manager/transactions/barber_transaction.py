from django.db import transaction
from django.core.exceptions import ValidationError
from account.models import Barber
from datetime import timedelta
from booking_manager.models import Booking

def change_barbers_transaction(booking_item, new_barber):
    with transaction.atomic():
       new_barber = Barber.objects.select_for_update().get(id=new_barber.id)
       old_barber = booking_item.barber

       if old_barber.id == new_barber.id:
           raise ValidationError({"barber": "You cannot transfer a booking to the same barber!"})

       time_to_visit = booking_item.visit_time
       duration = booking_item.booking_service.duration_minute
       time_to_finish = time_to_visit + timedelta(minutes=duration)

       close_bookings = Booking.objects.filter(barber=new_barber, is_active=True, visit_time__lt=time_to_finish)

       for other_book in close_bookings:
           if other_book.id == booking_item.id:
                continue
           other_book_finish = other_book.visit_time + timedelta(minutes=other_book.booking_service.duration_minute)

           if other_book_finish > time_to_visit:
               raise ValidationError({
                   "barber":f"Barber '{new_barber.user.first_name}' is busy! Overlap detected with booking #{other_book.id}."
               })

       booking_item.barber = new_barber
       booking_item.save()

    return booking_item

# Функция переноса существующего бронирования к другому барберу. Перед переносом проверяем,
# что новый барбер свободен в указанное время с учётом продолжительности услуги.
# Если время занято или возникает ошибка, первоначальные данные бронирования остаются неизменными.






