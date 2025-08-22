from django.urls import path
from .views import (
    CategoryListCreateView, CategoryListView,
    ProductListCreateView, ProductListView, ProductDetailView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryListCreateView.as_view(), name='category_create'),


    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductListCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
