from django.contrib import admin
from ..models import Comment

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
