import random
from datetime import timedelta
from django.utils import timezone
from booking_manager.models import Product, Promotion, PromotionBookingService

def create_products_promotions(fake, created_booking_services):
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
    for name in product_names:
        products.append(
            Product(
                name=name,
                description=fake.text(max_nb_chars=150),
                price=random.randint(10, 100) * 10,
                amount=random.randint(0, 100)
            )
        )

    created_products = Product.objects.bulk_create(products)

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

    created_promotions = Promotion.objects.bulk_create(promotion)

    # Добавдяем акции на услуги
    pbs = []
    services_count = len(created_booking_services)
    for pr in created_promotions:
        sample_size = min(services_count, random.randint(2, 5))
        un_services = random.sample(created_booking_services, sample_size) if sample_size > 0 else []
        for bs in un_services:
            pbs.append(
                PromotionBookingService(
                    promotion=pr,
                    booking_service=bs,
                    discount_percent=random.choice([5, 10, 20, 30, 50])
                )
            )
    PromotionBookingService.objects.bulk_create(pbs, ignore_conflicts=True)



    return  created_products, created_promotions
