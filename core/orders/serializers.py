from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'total_price', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=self.context['request'].user, **validated_data)
        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price * quantity
            total += price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
        order.total_price = total
        order.save()
        return order
