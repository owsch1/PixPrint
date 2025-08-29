from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display       = ("id", "title", "price", "created_at", "has_image")
    list_display_links = ("id", "title")
    search_fields      = ("title", "description")
    list_filter        = ("created_at",)
    ordering           = ("title",)
    readonly_fields    = ("created_at",)

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Image?"