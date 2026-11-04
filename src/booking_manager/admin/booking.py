from django.contrib import admin
from ..models import Booking, ProductBooking



class ProductBookingInline(admin.TabularInline):
    model = ProductBooking
    fields = ('product', 'quantity', 'get_total_cost')
    readonly_fields = ('get_total_cost',)
    extra = 3

    @admin.display(description="Общая стоимость")
    def get_total_cost(self, obj):
        if obj.product and obj.quantity:
            return obj.product.price * obj.quantity
        return 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["name", "visit_time", "is_active", "barber_name", "client_name", "booking_service_name", "booking_and_barber"]
    list_display_links = ("name", "visit_time")
    list_editable = ("is_active",)
    readonly_fields = ('created_at', 'total_products_cost')
    inlines = [
        ProductBookingInline
    ]
    search_fields = ("name", 'client__user__email', "barber__user__first_name")
    list_filter = ("visit_time", "is_active", "barber", 'booking_service')

    @admin.display(description="Общая стоимость товаров")
    def total_products_cost(self, obj):
        if not obj.pk:
            return 0

        total = sum(pb.product.price * pb.quantity for pb in obj.productbooking_set.all())
        return total

    @admin.display(empty_value="???")
    def barber_name(self, obj):
        if obj.barber:
            return obj.barber.user.first_name

    @admin.display(empty_value="???")
    def client_name(self, obj):
        if obj.client:
            return obj.client.user.first_name

    @admin.display(empty_value="???")
    def booking_service_name(self, obj):
        if obj.booking_service:
            return obj.booking_service.name

    @admin.display(empty_value="---", description="Мастер и Бронирование")
    def booking_and_barber(self, obj):
        if obj.barber:
            barber_name = obj.barber.user.first_name
            return f'{barber_name}, {obj.name}'
        return None
