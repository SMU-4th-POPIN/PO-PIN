from django.contrib import admin
from .models import Notice, NoticeImage

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_filter = ("is_pinned", "created_at")
    readonly_fields = ("created_at", "updated_at", "views")

admin.site.register(NoticeImage)