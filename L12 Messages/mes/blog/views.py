from django.contrib import messages
from django.db.models import Avg, Count, Min, Max, F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from .forms import ContactForm, PostForm, CommentForm
from .mixins import MessageHandlerFormMixin
from .models import Post, Author, Comment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    ordering = ['-created_at']


class CreatePostView(CreateView, MessageHandlerFormMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_message = 'Пост создан!'


class UpdatePostView(UpdateView, MessageHandlerFormMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    pk_url_kwarg = 'id'
    success_message = 'Пост обновлен!'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Пост удален!')
        return reverse_lazy('blog:post_list')


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'blog/author_detail.html'
    context_object_name = 'author'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('posts').annotate(
            post_count=Count('posts')
        )


def create_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = Author.objects.first()
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('blog:post_detail', post.id)
        else:
            messages.error(request, 'Что-то пошло не так...')
    return redirect('blog:post_detail', post.id)


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Комментарий удален!')
        return reverse_lazy('blog:post_detail', kwargs={'id': self.object.post.id})


def contacts(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Спасибо за обратную связь!')
            print(form.cleaned_data)
            return redirect('blog:contacts')
        else:
            messages.error(request, 'Что-то пошло не так...')
            form.add_error(None, 'Form is not valid')
            return redirect('blog:contacts')

    form = ContactForm()
    return render(request, 'blog/contacts.html', {'form': form})
