from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer  # <-- zentraler Serializer

class ProductSerializer(serializers.ModelSerializer):
    # DE: Kategorie verschachtelt (read-only)
    # RU: Вложенная категория (только для чтения)
    category = CategorySerializer(read_only=True)

    # DE: Schreiben per ID
    # RU: Запись по ID
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Product._meta.get_field('category').remote_field.model.objects.all(),
        source='category',
        write_only=True
    )

    # ... deine restlichen Felder (image_url/owner etc.) bleiben wie gehabt ...
    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "image", "category", "category_id", "created_at"]
        read_only_fields = ["created_at"]