from django.urls import path
from .views import ProductListView, ProductListCreateView, ProductDetailView

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("create/", ProductListCreateView.as_view(), name="product_create"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]