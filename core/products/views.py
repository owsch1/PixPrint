from rest_framework import generics, permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# ---------- CATEGORIES ----------
class CategoryListView(generics.ListAPIView):
    """
    DE: Öffentliche Liste der Kategorien
    RU: Публичный список категорий
    """
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    DE: Liste + Erstellen (nur Admin darf POST)
    RU: Список + создание (POST только для администратора)
    """
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer

    def get_permissions(self):
        # DE: GET für alle, POST nur für Admin
        # RU: GET для всех, POST только админ
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DE: Lesen/Ändern/Löschen einer Kategorie (nur Admin darf ändern/löschen)
    RU: Получение/редактирование/удаление категории (редактировать/удалять может только админ)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


# ---------- PRODUCTS ----------
class ProductListView(generics.ListAPIView):
    """
    DE: Öffentliche Liste der Produkte
    RU: Публичный список продуктов
    """
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductListCreateView(generics.ListCreateAPIView):
    """
    DE: Liste + Erstellen (nur Admin darf POST)
    RU: Список + создание (POST только для администратора)
    """
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer

    def get_permissions(self):
        # DE: GET für alle, POST nur Admin
        # RU: GET для всех, POST только админ
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DE: Lesen/Ändern/Löschen eines Produkts (nur Admin darf ändern/löschen)
    RU: Получение/редактирование/удаление продукта (редактировать/удалять может только админ)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]