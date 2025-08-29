# orders/serializers.py
from decimal import Decimal
from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    # DE: Vollständiges Produkt nur zum Lesen (für die Antwort)
    # RU: Полный объект продукта только для чтения (в ответе)
    product = ProductSerializer(read_only=True)

    # DE: Bei der Erstellung nur die ID schicken; mappt auf 'product'
    # RU: При создании передаём только ID; маппится на 'product'
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']
        # DE: Preis wird serverseitig berechnet → nur read-only
        # RU: Цена вычисляется на сервере → только для чтения
        read_only_fields = ['price']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    # DE: User als Text (z. B. email) nur lesen
    # RU: Пользователь как строка (например email), только для чтения
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'total_price', 'items']
        read_only_fields = ['created_at', 'total_price']

    def validate_items(self, value):
        # DE: Mindestens 1 Position
        # RU: Минимум 1 позиция
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        # DE: Items aus den Daten nehmen
        # RU: Извлекаем позиции из данных
        items_data = validated_data.pop('items', [])

        # ⚠️ WICHTIG: 'user' robust ermitteln — entweder aus validated_data (falls perform_create serializer.save(user=...) nutzt)
        #             oder aus dem Request-Kontext. So vermeiden wir "multiple values for keyword argument 'user'".
        user = validated_data.pop('user', None) or self.context['request'].user

        # DE: Bestellung anlegen
        # RU: Создаём заказ
        order = Order.objects.create(user=user, **validated_data)

        # DE: Summe in Decimal
        # RU: Сумма в Decimal
        total = Decimal('0')

        # DE: Positionen anlegen + Preis berechnen
        # RU: Создаём позиции + считаем цену
        for item in items_data:
            product = item['product']  # dank source='product' bereits Product-Objekt
            quantity = item['quantity']
            line_price = (product.price or Decimal('0')) * quantity
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=line_price
            )
            total += line_price

        # DE: Gesamtsumme speichern
        # RU: Сохраняем общую сумму
        order.total_price = total
        order.save(update_fields=['total_price'])

        return order