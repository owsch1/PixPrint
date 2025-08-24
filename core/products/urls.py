from django.urls import path
from .views import ProductListView, ProductListCreateView, ProductDetailView

urlpatterns = [
    # DE: Öffentliche Produktliste / RU: Публичный список продуктов
    path("", ProductListView.as_view(), name="product_list"),

    # DE: Produkt erstellen (POST nur Admin) / RU: Создание продукта (POST только админ)
    path("create/", ProductListCreateView.as_view(), name="product_create"),

    # DE: Detail/Ändern/Löschen / RU: Детали/изменение/удаление
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]