from django.db import transaction
from django.core.exceptions import ValidationError
from booking_manager.models import ProductBooking, Product

def create_product_booking_transaction(booking_item, product, quantity):
    with transaction.atomic():
        product_for_change = Product.objects.select_for_update().get(id=product.id)

        if product_for_change.amount < quantity:
            raise ValidationError(
                {
                    "quantity": f"Not enough stock for '{product_for_change.name}'! Only {product_for_change.amount} items available."}
            )
        product_for_change.amount -= quantity
        product_for_change.save()

        product_booking = ProductBooking.objects.create(
            booking=booking_item,
            product=product,
            quantity=quantity,
            total_price=quantity * product.price
        )

    return product_booking

# Функция, которая создаёт бронирование, добавляет к нему несколько товаров через ProductBooking и уменьшает их количество.
# Все операции выполняются в одной транзакции. Если хотя бы одного товара недостаточно, отменяются все изменения,
# включая создание бронирования.
