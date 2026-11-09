import random
from booking_manager.models import Barbershop, BookingService
from booking_manager.constants import CategoryChoices


def create_booking_services_barbershops(fake):
    # Создание 5 барбершопов
    barbershops = []
    barb_names = ['Brills', 'Hard', 'OldBoy', 'Hardmen', 'Big Bro']
    for name in barb_names:
        barbershop = Barbershop(
            name=name,
            phone=f'+37544{random.randint(1000000, 9999999)}',
            address=f"{fake.city()},{fake.street_address()}",
            description=fake.text(max_nb_chars=150)
        )
        barbershops.append(barbershop)

    created_barbershops = Barbershop.objects.bulk_create(barbershops)

    # Создание 20 услуг
    bs = []
    bs_names = [
        "Мужская стрижка ",
        "Стрижка Fade (Фейд)",
        "Стрижка под машинку",
        "Детская стрижка",
        "Моделирование бороды",
        "Камуфляж бороды",
        "Королевское бритье",
        "Удаление волос воском (Ваксинг) ",
        "Черная маска (Black Mask)",
        "Комплекс «Стрижка + Борода»",
    ]
    for i in range(20):
        bs.append(
            BookingService(
                name=random.choice(bs_names),
                description=fake.text(max_nb_chars=150),
                price=random.randint(10, 50) * 5,
                duration_minute=random.choice([30, 45, 60, 90, 120]),
                category=random.choice(CategoryChoices.values),
            )
        )

    created_booking_services = BookingService.objects.bulk_create(bs)

    return created_barbershops, created_booking_services



