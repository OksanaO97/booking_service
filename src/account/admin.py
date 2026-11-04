from django.contrib import admin
from .models import User, Client, Barber
from booking_manager.models import Comment

admin.site.register(User)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "user__username", "user__first_name")
    list_display = ("id", "user", "status", "date_of_birth")


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('author_name',)
    fields = ('author_name', 'text', 'rating', 'is_published')
    extra = 3


    @admin.display(description="Автор", empty_value="???")
    def author_name(self, obj):
        if obj.client and obj.client.user and obj.client.user.first_name:
            return obj.client.user.first_name
        return 'Автора нет'


@admin.register(Barber)
class BarberServiceAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
