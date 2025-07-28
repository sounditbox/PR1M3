from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_spam, CommentMaxLengthValidator


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),

    )
    PUBLISHED = 'published'
    DRAFT = 'draft'
    ARCHIVED = 'archived'
    DELETED = 'deleted'

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PUBLISHED)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(get_user_model(), related_name='posts',
                               on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='posts',
                                 on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'title'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/posts/{self.id}'


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(get_user_model(), related_name='comments',
                               on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_spam,
                                           CommentMaxLengthValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']




class Tag(models.Model):
    title = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.title
