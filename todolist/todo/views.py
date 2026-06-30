from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm

def task_list(request) -> HttpResponse:
    """Главная страница со списком всех задач."""
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "todo/task_list.html", context)

def task_create(request) -> HttpResponseRedirect | HttpResponse:
    """Добавление новой задачи."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
        context = {"form": form}
    return render(request, "todo/task_form.html", context)

@require_POST
def task_toggle_done(request, pk) -> HttpResponseRedirect:
    """Переключение статуса is_done (только POST)."""
    task = get_object_or_404(Task, pk=pk)
    task.is_done = not task.is_done
    task.save()
    return redirect("task_list")

@require_POST
def task_delete(request, pk) -> HttpResponseRedirect:
    """Удаление задачи (только POST)."""
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("task_list")