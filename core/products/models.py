from django.db import models

class Category(models.Model):
    # DE: Kategorie mit optionalem Bild
    # RU: Категория с необязательной картинкой
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    # DE: Produkt inkl. optionalem Bild und Erstellzeitpunkt
    # RU: Продукт с необязательной картинкой и датой создания
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # leer erlaubt / допускается пустое
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title