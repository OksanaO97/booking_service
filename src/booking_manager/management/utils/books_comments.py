import random
from datetime import timedelta
from django.utils import timezone
from booking_manager.models import Booking, ProductBooking, Comment

def create_bookings_comments(fake, created_barbers, created_clients, created_booking_services, created_products):
    # Создание 500 бронирований
    bookings = []
    for i in range(500):
        random_days = random.randint(-30, 30)
        visit_time = timezone.now() + timedelta(days=random_days, hours=random.randint(-4, 6))
        bookings.append(
            Booking(
                name=f'Бронирование{i}',
                visit_time=visit_time,
                client=random.choice(created_clients),
                barber=random.choice(created_barbers),
                booking_service=random.choice(created_booking_services)
            )
        )
    created_bookings = Booking.objects.bulk_create(bookings)

    # Добавляем товары бронированиям
    product_bookings = []
    for booking in created_bookings:
        if random.choice([True, False, False]):
            un_products = random.sample(created_products, random.randint(1, 3))
            for prod in un_products:
                quantity = random.choice([1, 2, 3])
                product_bookings.append(
                    ProductBooking(
                        product=prod,
                        booking=booking,
                        quantity=quantity,
                        total_price=float(prod.price * quantity)
                    )
                )
    ProductBooking.objects.bulk_create(product_bookings)

    comments = []
    com_texts = [
        "Отличная работа, мастер знает свое дело!",
        "Стрижка супер, приду еще раз обязательно.",
        "Все понравилось, сервис на высшем уровне.",
        "Барбер отличный, подсказал крутую укладку.",
        "Сделали все быстро, аккуратно и очень стильно.",
        "Атмосфера в салоне топовая, кофе вкусный!",
        "Мастер вежливый, борода выглядит идеально.",
        "Лучший барбершоп в городе, стригусь только тут."
    ]
    un_bookings = random.sample(created_bookings, 200)
    for booking in un_bookings:
        comments.append(
            Comment(
                text=random.choice(com_texts),
                client=booking.client,
                barber=booking.barber,
                booking=booking,
                rating=random.randint(1, 5)
            )
        )
    Comment.objects.bulk_create(comments)

