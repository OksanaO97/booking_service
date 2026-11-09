from django.db import transaction
from django.core.exceptions import ValidationError
from booking_manager.models import ProductStock

def move_product_transaction(product_id, barbershop_from, barbershop_to, quantity):
    if quantity <= 0:
       raise ValidationError({'quantity':'The quantity cannot be negative or equal to 0'})

    if barbershop_to.id == barbershop_from.id:
        raise ValidationError('Source and destination barbershops cannot be the same')

    first_id, second_id = sorted([barbershop_from.id, barbershop_to.id])

    with transaction.atomic():
        try:

            first_stock = ProductStock.objects.select_for_update().get(product_id=product_id, barbershop_id=first_id)
            second_stock = ProductStock.objects.select_for_update().get(product_id=product_id, barbershop_id=second_id)

        except ProductStock.DoesNotExist:
            raise ValidationError("The specified product is not registered at one of the barbershops.")

        if first_stock.barbershop_id == barbershop_from.id:
            stock_from = first_stock
            stock_to = second_stock
        else:
            stock_from = second_stock
            stock_to = first_stock

        if stock_from.stock < quantity:
            raise ValidationError({
                'quantity':f"Not enough stock at the source barbershop! Available: {stock_from.stock} items, requested: {quantity} items."
            })

        stock_from.stock -= quantity
        stock_to.stock += quantity

        stock_from.save()
        stock_to.save()

    return stock_from, stock_to


# Функция перемещения товара между двумя филиалами.
# Если товара недостаточно или возникает ошибка, остатки обоих филиалов остаются неизменными.
# Предусмотрен одинаковый порядок блокировки записей для снижения риска взаимной блокировки.
