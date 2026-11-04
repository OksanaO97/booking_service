from django.contrib import admin
from ..models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "amount"]
    list_editable = ("price", "amount")
    search_fields = ("name", )
    actions = ['change_amount_product']

    @admin.action(description="Увеличивать количество выбранных товаров на 10")
    def change_amount_product(self, request, queryset):
        for product in queryset:
            product.amount += 10
            product.save(update_fields=['amount'])
