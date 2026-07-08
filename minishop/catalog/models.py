from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="products", verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)], verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self) -> str:
        return self.name