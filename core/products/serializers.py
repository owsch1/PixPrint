from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # отдадим абсолютный URL картинки в поле img
    img = serializers.SerializerMethodField()

    class Meta:
        model  = Product
        fields = ["id", "img", "title", "description", "price", "discount"]

    def get_img(self, obj):
        request = self.context.get("request")
        if obj.img:
            url = obj.img.url
            return request.build_absolute_uri(url) if request else url
        return None

    def validate_discount(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Скидка должна быть от 0 до 100.")
        return value