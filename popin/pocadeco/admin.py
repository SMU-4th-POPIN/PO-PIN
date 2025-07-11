from django.contrib import admin
from .models import DecoratedPhotocard, StickerPlacement

class StickerPlacementInline(admin.TabularInline):
    model = StickerPlacement
    extra = 1

@admin.register(DecoratedPhotocard)
class DecoratedPhotocardAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at")
    search_fields = ("title", "user__username")
    list_filter = ("created_at",)
    inlines = [StickerPlacementInline]

@admin.register(StickerPlacement)
class StickerPlacementAdmin(admin.ModelAdmin):
    list_display = ("emoji", "photocard", "x", "y", "scale", "rotation")
    search_fields = ("emoji", "photocard__title")
    list_filter = ("photocard",)