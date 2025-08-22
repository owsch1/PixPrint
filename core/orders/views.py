from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

class OrderPayView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user:
            return Response({'detail': 'Нет доступа'}, status=status.HTTP_403_FORBIDDEN)
        order.status = 'paid'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
