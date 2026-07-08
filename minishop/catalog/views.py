from typing import Any
from django.db.models.manager import BaseManager
from django.views.generic import ListView, DetailView
from .models import Product, Category

class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self) -> BaseManager[Product]:
        queryset = Product.objects.select_related("category").all()

        # Получаем параметры из GET-запроса
        search_query = self.request.GET.get("q", "")
        category_id = self.request.GET.get("category", "")
        price_from = self.request.GET.get("price_from", "")
        price_to = self.request.GET.get("price_to", "")

        # Поиск по названию (регистронезависимый)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        # Фильтр по категории
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Фильтр по цене "от" и "до"
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)
        return queryset
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Передаём в шаблон все категории для выпадающего списка
        context["categories"] = Category.objects.all()

        # Передаём выбранные значения, чтобы сохранить их в форме после отправки
        context["current_q"] = self.request.GET.get("q", "")
        context["current_category"] = self.request.GET.get("category", "")
        context["current_price_from"] = self.request.GET.get("price_from", "")
        context["current_price_to"] = self.request.GET.get("price_to", "")
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"