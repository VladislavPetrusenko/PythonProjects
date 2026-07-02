from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

def post_list(request) -> HttpResponse:
    """Главная страница – только опубликованные посты"""
    posts = Post.objects.filter(status="published")
    context = {"posts": posts}
    return render(request, "blog/post_list.html", context=context)

def post_detail(request, pk) -> HttpResponse:
    """Просмотр одного поста"""
    post = get_object_or_404(Post, pk=pk)
    context = {"post": post}
    return render(request, "blog/post_detail.html", context=context)

def post_create(request) -> HttpResponseRedirect | HttpResponse:
    """Создание нового поста"""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
        context = {"form": form}
    return render(request, "blog/post_form.html", context=context)

def post_update(request, pk) -> HttpResponseRedirect | HttpResponse:
    """Редактирование поста"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {"form": form}
    return render(request, "blog/post_form.html", context=context)

def post_delete(request, pk) -> HttpResponseRedirect | HttpResponse:
    """Удаление поста с подтверждением"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    context = {"post": post}
    return render(request, "blog/post_confirm_delete.html", context=context)