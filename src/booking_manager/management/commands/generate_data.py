import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.models import Barber, Client
from booking_manager.models import Barbershop, BookingService, Booking, Product, ProductBooking, Comment, Promotion, PromotionBookingService
from booking_manager.constants import CategoryChoices
from datetime import timedelta
from django.utils import timezone


User = get_user_model()
fake = Faker("ru_RU")

class Command(BaseCommand):


    def handle(self, *args, **options):
        # Создание 100 пользователей
        users = []
        for i in range(100):
            user = User(
                username=f'{fake.unique.user_name()}{i}',
                phone=f'+37544{random.randint(1000000, 9999999)}',
                first_name=fake.first_name_female() if i % 33 == 0 else fake.first_name_male(),
                last_name=fake.last_name_female() if i % 33 == 0 else fake.last_name_male(),
                email=fake.unique.email()
            )
            user.set_password(fake.password(length=8, special_chars=False))
            users.append(user)
        User.objects.bulk_create(users)
        all_users = list(User.objects.all())


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
        Barbershop.objects.bulk_create(barbershops)
        all_barbershops = list(Barbershop.objects.all())


        # Создание 15 барберов
        barbers = []
        for i in range(15):
            barbers.append(
                Barber(
                    user=all_users[i],
                    barbershop=random.choice(all_barbershops),
                    experience_year=random.randint(1, 10)
                )
            )
        Barber.objects.bulk_create(barbers)
        all_barbers = list(Barber.objects.all())


        # Создание 80 клиентов
        clients = []
        for i in range(15, 95):
            clients.append(
                Client(
                    status=random.choice(['noob', 'beginner', 'expert', 'legend']),
                    date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
                    user = all_users[i]
                )
            )
        Client.objects.bulk_create(clients)
        all_clients = list(Client.objects.all())

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
        BookingService.objects.bulk_create(bs)
        all_booking_services = list(BookingService.objects.all())

        # Создание 500 бронирований
        bookings = []
        for i in range(500):
            random_days = random.randint(-30, 30)
            visit_time = timezone.now() + timedelta(days=random_days, hours=random.randint(-4, 6))
            bookings.append(
                Booking(
                    name=f'Бронирование{i}',
                    visit_time=visit_time,
                    client=random.choice(all_clients),
                    barber=random.choice(all_barbers),
                    booking_service=random.choice(all_booking_services)
                )
            )
        Booking.objects.bulk_create(bookings)
        all_bookings = list(Booking.objects.all())

        # Создание 50 товаров
        product_names = [
            "Шампунь для глубокой очистки",
            "Кондиционер для увлажнения",
            "Масло для ухода за бородой",
            "Матирующий воск",
            "Гель для точного бритья",
            "Тоник для кожи головы",
            "Спрей с морской солью",
            "Глина для сильной фиксации",
            "Шампунь для жирной кожи",
            "Воск для усов",
            "Одеколон",
            "Лосьен после бритья",
            "Щетка для бороды",
            "Расческа для бороды",
        ]
        products = []
        for i in range(50):
            products.append(
                Product(
                    name=random.choice(product_names),
                    description=fake.text(max_nb_chars=150),
                    price=random.randint(10, 100) * 10,
                    amount=random.randint(0, 100)
                )
            )
        Product.objects.bulk_create(products)
        all_products = list(Product.objects.all())


        # Добавляем товары бронированиям
        product_bookings = []
        for booking in all_bookings:
            if random.choice([True, False, False]):
                un_products = random.sample(all_products, random.randint(1, 3))
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



        # Создание 200 комментариев
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
        un_bookings = random.sample(all_bookings, 200)
        for booking in un_bookings:
            comments.append(
                Comment(
                    text=random.choice(com_texts),
                    client=booking.client,
                    barber=booking.barber,
                    booking=booking
                )
            )
        Comment.objects.bulk_create(comments)



        # Создание 10 акций
        promotion = []
        pr_list = ['Черная пятница', 'Утренние часы', 'День Рождения', 'Первый визит',
                   'Отец + Сын', 'Новый год', 'Неделя бороды', 'Студентам', 'Зимний уход',
                   'Приведи друга']
        for pr in pr_list:
            start_date = timezone.now().date() - timedelta(days=7)
            end_date = timezone.now().date() + timedelta(days=random.randint(5, 25))
            promotion.append(
                Promotion(
                    name=pr,
                    description=fake.text(max_nb_chars=150),
                    start_date=start_date,
                    end_date=end_date
                )
            )
        Promotion.objects.bulk_create(promotion)
        all_promotion = list( Promotion.objects.all())



            # Добавдяем акции на услуги
        pbs = []
        for pr in all_promotion:
            un_services = random.sample(all_booking_services, random.randint(2, 5))
            for bs in un_services:
                pbs.append(
                    PromotionBookingService(
                        promotion=pr,
                        booking_service=bs,
                        discount_percent=random.choice([5, 10, 20, 30, 50])
                    )
                )
        PromotionBookingService.objects.bulk_create(pbs)


        self.stdout.write(self.style.SUCCESS("New data created"))




































