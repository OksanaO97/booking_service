from django.contrib import admin
from ..models import Barbershop

@admin.register(Barbershop)
class BarbershopAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "phone", "description", "opening_time", "closing_time", "is_active"]
    search_fields = ("name", "address")