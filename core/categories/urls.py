from django.urls import path
from .views import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    # DE: Liste + Erstellen / RU: Список + Создание
    path("", CategoryListCreateView.as_view(), name="category_list_create"),
    # DE: Detail/Ändern/Löschen / RU: Детали/изменение/удаление
    path("<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
]