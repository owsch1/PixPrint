# DE: Produkte im Admin registrieren
# RU: Регистрация продуктов в админке
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "description")
    ordering = ("-created_at",)