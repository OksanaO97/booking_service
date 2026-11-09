from django.contrib import admin
from ..models import Promotion, PromotionBookingService


class PromotionBookingServiceInline(admin.TabularInline):
    model = PromotionBookingService
    extra = 3

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "start_date", "end_date", "is_active"]
    actions = ['change_is_active']
    inlines = [PromotionBookingServiceInline]

    @admin.action(description="Активировать и деактивировать выбранные акции")
    def change_is_active(self, request, queryset):
        for promotion in queryset:
            promotion.is_active = not promotion.is_active
            promotion.save(update_fields=['is_active'])