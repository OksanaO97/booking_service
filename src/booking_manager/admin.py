from django.contrib import admin
from .models import Barbershop, BookingService, Booking, Product, ProductBooking, Comment, Promotion, PromotionBookingService


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



@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "duration_minute", "is_active"]
    search_fields = ("name", "description")


@admin.register(Barbershop)
class BarbershopAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "phone", "description", "opening_time", "closing_time", "is_active"]
    search_fields = ("name", "address")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", "is_published", "rating"]
    list_filter = ("is_published", "rating")
    actions = ['change_is_published']

    @admin.action(description="Публиковать и скрывать выбранные комментарии")
    def change_is_published(self, request, queryset):
        for comment in queryset:
            comment.is_published = not comment.is_published
            comment.save(update_fields=['is_published'])



@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "start_date", "end_date", "is_active"]
    actions = ['change_is_active']

    @admin.action(description="Активировать и деактивировать выбранные акции")
    def change_is_active(self, request, queryset):
        for promotion in queryset:
            promotion.is_active = not promotion.is_active
            promotion.save(update_fields=['is_active'])


@admin.register(  ProductBooking, PromotionBookingService)
class OtherAdmin(admin.ModelAdmin):
    pass





# class EmailExistListFilter(admin.SimpleListFilter):
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = "Заведена ли почта у барбера"
#
#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = "decade"
#
#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return [
#             ("exist", "barber email exist"),
#             ("not exist", "barber email not exist"),
#         ]
#
#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         # Compare the requested value (either '80s' or '90s')
#         # to decide how to filter the queryset.
#         if self.value() == "exist":
#             return queryset.filter(barber__user__email__isnull=False)
#         if self.value() == "not exist":
#             return queryset.filter(barber__user__email__isnull=True)







#
# class ProductInline(admin.TabularInline):
#     model = Product.bookings.through



# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ["name", "is_active", "visit_time", "created_at", "barber_name"]
#     # exclude = ["is_active"]
#     fields = ["name", "is_active", "visit_time", "booking_service", ("barber", "client")]
#     list_editable = ("is_active", )
#     list_display_links = ("name", "barber_name")
#     list_filter = ("visit_time", "is_active", EmailExistListFilter)
#     ordering = ("-visit_time",)
#     search_fields = ("name",)
#     list_per_page = 10
#     inlines = [
#         ProductInline
#     ]
#     actions = ['make_is_active', 'make_default_barber']
#
#     @admin.action(description="Активировать выбранные записи")
#     def make_is_active(self, request, queryset):
#         queryset.update(is_active=True)
#
#     @admin.action(description="Активировать изменение последних барберов")
#     def make_default_barber(self, request, queryset):
#         barber = Barber.objects.last()
#         queryset.update(barber=barber)


    # fieldsets = [
    #     (
    #         None,
    #         {
    #             "fields": ["name", "is_active", "visit_time"],
    #         },
    #     ),
    #     (
    #         "Advanced options",
    #         {
    #             "classes": ["collapse"],
    #             "fields": ["barber", "client"],
    #         },
    #     ),
    # ]


#
#     @admin.display(empty_value="???")
#     def barber_name(self, obj):
#         if obj.barber:
#             return obj.barber.user.first_name
#
#
#
#
# class BookingInline(admin.TabularInline):
#     model = Booking
#     extra = 3
#
#
# @admin.register(BookingService)
# class BookingServiceAdmin(admin.ModelAdmin):
#     inlines = [
#         BookingInline,
#     ]


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     filter_horizontal = ["bookings"]
