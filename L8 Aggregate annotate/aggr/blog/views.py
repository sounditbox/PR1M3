from django.db.models import Avg, Count, Min, Max, F, Value
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from .models import Post, Comment, Author


class IndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Post.objects.aggregate(
            total_posts=Count('pk'),
            average_views=Avg('views'),
            min_views=Min('views'),
            max_views=Max('views'),
            unique_authors=Count('author', distinct=True)
        )
        stats['average_views'] = round(stats['average_views'], 2)
        context['stats'] = stats
        context['categories'] = Post.objects.values('category__title')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().annotate(
            annotated_views=F('views') + 1
        )

    def get_object(self, queryset=None):
        obj: Post = super().get_object(queryset)
        obj.views = F('views') + 1
        obj.save(update_fields=['views'])
        return obj


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


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'blog/author_detail.html'
    context_object_name = 'author'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('posts').annotate(
            post_count=Count('posts')
        )


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
