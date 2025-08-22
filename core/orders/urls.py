from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderPayView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/pay/', OrderPayView.as_view(), name='order_pay'),
]
