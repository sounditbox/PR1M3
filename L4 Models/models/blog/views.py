from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Post


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'blog/index.html')


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = Post.objects.get(id=id)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/post_list.html', context)


@require_POST
def create_post(request: HttpRequest) -> HttpResponse:
    title = request.POST.get('title')
    content = request.POST.get('content')
    is_published = request.POST.get('is_published') == 'on'
    post = Post.objects.create(title=title, content=content,
                               is_published=is_published)
    return redirect('blog:post_detail', post.id)


def update_post(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=id)
    post.title = request.POST.get('title', post.title)
    post.content = request.POST.get('content', post.content)
    post.is_published = request.POST.get('is_published', post.is_published)
    post.save()
    return redirect('blog:post_detail', post.id)


def delete_post(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('blog:post_list')
