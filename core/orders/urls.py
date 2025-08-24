from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderPayView

urlpatterns = [
    path("", OrderListCreateView.as_view(), name="order_list_create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("<int:pk>/pay/", OrderPayView.as_view(), name="order_pay"),
]