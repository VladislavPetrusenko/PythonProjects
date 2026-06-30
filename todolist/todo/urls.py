from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("add/", views.task_create, name="task_create"),
    path("<int:pk>/toggle/", views.task_toggle_done, name="task_toggle_done"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete")
]