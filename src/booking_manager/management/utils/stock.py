import random
from booking_manager.models import ProductStock


def create_stock(fake, created_barbershops, created_products):
    # Создание стоков
    stocks = []
    for barbershop in created_barbershops:
        for product in created_products:
            stock = ProductStock(
                product=product,
                barbershop=barbershop,
                stock=random.randint(1, 10)
            )
            stocks.append(stock)

    created_stocks = ProductStock.objects.bulk_create(stocks, ignore_conflicts=True)
    return created_stocks

