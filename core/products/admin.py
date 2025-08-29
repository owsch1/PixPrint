from django import forms
from django.contrib import admin
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels = {"price": "Price (KGS)"}
        help_texts = {"price": "Сумма в киргизских сомах (KGS)."}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display  = ("id", "title", "price_kgs", "discount", "created_at")
    list_filter   = ("discount", "created_at")
    search_fields = ("title", "description")
    ordering      = ("-created_at",)
    inlines       = [ProductImageInline]

    def price_kgs(self, obj):
        return f"{obj.price:,.2f} KGS"
    price_kgs.short_description = "Price"