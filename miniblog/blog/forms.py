from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "status"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5})
        }
        labels = {
            "title": "Заголовок",
            "content": "Текст",
            "status": "Статус"
        }
    
    def clean_content(self):
        content = self.cleaned_data.get("content", "")
        if content and len(content) < 1:
            raise ValidationError("Текст должен содержать не менее 1 символов.")
        return content