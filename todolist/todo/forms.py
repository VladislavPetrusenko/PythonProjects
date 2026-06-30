from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "is_done"]
        labels = {
            "title": "Название",
            "description": "Описание",
            "is_done": "Выполнено"
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3})
        }