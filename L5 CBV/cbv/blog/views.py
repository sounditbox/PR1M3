from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from .models import Post


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


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    ordering = ['-created_at']


class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'content', 'is_published']
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
