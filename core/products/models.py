from django.db import models

class Product(models.Model):
    # id создаётся автоматически
    img         = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Изображение")
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=12, decimal_places=2)
    discount    = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Скидка в %, 0–100")

    # оставил для админ-удобства; во фронт не отдаём
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey("Product", related_name="images", on_delete=models.CASCADE)
    image   = models.ImageField(upload_to="products/gallery/")
    alt     = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return f"{self.product_id} - {self.image.name}"