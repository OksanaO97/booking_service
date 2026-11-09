from django.contrib import admin
from ..models import BookingService

@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "duration_minute", "is_active"]
    search_fields = ("name", "description")
