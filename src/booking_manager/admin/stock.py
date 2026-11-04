from django.contrib import admin
from ..models import ProductStock

@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ["product", "barbershop", "stock"]
    search_fields = ("product", "barbershop")