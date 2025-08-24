# DE: Bestellungen + Positionen im Admin registrieren (mit Inline)
# RU: Регистрация заказов и позиций в админке (через inline)
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "quantity", "price")
    readonly_fields = ("price",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email",)
    ordering = ("-created_at",)
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    list_filter = ("product",)
    search_fields = ("order__id", "product__title")