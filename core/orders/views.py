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
        # DE: Nur Bestellungen des eingeloggten Users
        # RU: Только заказы текущего пользователя
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # DE: User automatisch setzen
        # RU: Привязываем заказ к пользователю автоматически
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """
    DE: Einzelne Bestellung – доступ только владельцу (через фильтр QuerySet).
    RU: Просмотр конкретного заказа — только владелец видит.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # DE/RU: Ограничиваем выборку только своими заказами
        return Order.objects.filter(user=self.request.user)


class OrderPayView(generics.UpdateAPIView):
    """
    DE: Оплата заказа — только владелец. Запрос идемпотентен.
    RU: Оплата заказа — только владелец. Повторный вызов безопасен.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # DE/RU: Пользователь видит и может обновлять только свои заказы
        return Order.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()  # уже гарантированно свой заказ
        if order.status == "paid":
            # DE: Уже оплачен — просто вернём текущее состояние (идемпотентно)
            # RU: Уже оплачен — возвращаем текущее состояние (идемпотентность)
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        order.status = "paid"
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)