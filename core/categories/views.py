from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    DE: Liste für alle sichtbar (GET), Erstellen nur für Admin (POST).
    RU: Список доступен всем (GET), создание только для администратора (POST).
    """
    queryset = Category.objects.all().order_by("title")
    serializer_class = CategorySerializer

    def get_permissions(self):
        # DE: GET erlaubt allen, POST nur Admin
        # RU: GET для всех, POST только админ
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DE: Anzeigen/Ändern/Löschen – ändern/löschen nur für Admin.
    RU: Просмотр/изменение/удаление – изменять/удалять может только админ.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        # DE: GET für alle, PATCH/DELETE nur Admin
        # RU: GET для всех, PATCH/DELETE только админ
        if self.request.method in ["PATCH", "PUT", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]