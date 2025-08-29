# core/orders/views.py
from typing import Any
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """
    DE: Eigene Bestellungen auflisten/erstellen (только свои заказы).
    RU: Список/создание заказов текущего пользователя.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Wichtig:
        - Für anonyme Requests (Swagger-Schema, /) darf NICHT mit AnonymousUser gefiltert werden,
          sonst crasht es bei DEBUG=False. Deshalb: leeres QuerySet zurückgeben.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer: OrderSerializer) -> None:
        # DE: User automatisch setzen / RU: Привязка заказа к текущему пользователю
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """
    DE: Einzelne Bestellung – Zugriff nur für den Besitzer.
    RU: Просмотр заказа — только владелец.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user=user)


class OrderPayView(generics.UpdateAPIView):
    """
    DE: Zahlung des Auftrags — nur Besitzer. Idempotent.
    RU: Оплата заказа — только владелец. Идемпотентно.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user=user)

    def update(self, request, *args: Any, **kwargs: Any) -> Response:
        # get_object() nutzt das o.g. gefilterte QuerySet → nur eigene Orders
        order = self.get_object()

        if order.status == "paid":
            # Bereits bezahlt → idempotent den aktuellen Stand liefern
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        order.status = "paid"
        order.save(update_fields=["status"])
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)