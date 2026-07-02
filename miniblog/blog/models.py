from django.db import models

class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Черновик"),
        ("published", "Опубликовано")
    ]
    
    title = models.CharField(max_length=200, null=False, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст поста")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft",
                                            verbose_name="Статус")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата обновления")
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return self.title