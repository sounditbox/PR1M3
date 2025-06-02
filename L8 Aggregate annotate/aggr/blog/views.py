from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from .models import Post, Comment, Author


class IndexView(TemplateView):
    template_name = 'blog/index.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    ordering = ['-created_at']


class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'content', 'is_published', 'author']
    template_name = 'blog/post_create.html'


class UpdatePostView(UpdateView):
    model = Post
    fields = ['title', 'content', 'is_published']
    template_name = 'blog/post_edit.html'
    pk_url_kwarg = 'id'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')


class SimpleView(View):
    message = "Default message"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponse(self.message)


def create_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(content=request.POST.get('content'),
                                     author=Author.objects.first(),
                                     post=post)
    return redirect('blog:post_detail', post.id)
