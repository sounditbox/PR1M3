from django.contrib import admin

# Register your models here.
from .models import Post, Author, Tag, Category, Comment


class InlineComment(admin.StackedInline):
    model = Comment
    extra = 0
    fields = ('author', 'content', 'created_at', 'updated_at')
    readonly_fields = ('author', 'content', 'created_at', 'updated_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'status', 'updated', 'created_at', 'author', 'category')
    list_display_links = ('id',)
    list_editable = ('title', 'status', 'category', 'author')
    list_filter = ('author', 'category')
    list_select_related = ('author', 'category')
    search_fields = ('title', 'content')
    actions = ['publish', 'make_draft']
    inlines = [InlineComment]

    # fields = ('title', 'content', 'is_published', 'author', 'category')
    # exclude = ('views', 'annotated_views')
    fieldsets = (
        ('Основная информация', {  # Первый филдсет
            'fields': ('title', 'author', 'status', 'category'),
        }),
        ('Содержимое поста', {  # Второй филдсет
            'fields': ('content', 'views',),
            'classes': ('collapse',),  # Сделать блок сворачиваемым
            'description': 'Основной текст и теги для поста.'
        }),
        ('Даты (Авто)', {  # Третий филдсет
            'fields': ('created_at', 'updated'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('views', 'created_at', 'updated')

    @admin.display(description='updated')
    def updated(self, post: Post):
        return 'Not updated' if post.updated_at == post.created_at else post.updated_at

    def publish(self, request, queryset):
        self.message_user(request, 'Пост опубликован')
        queryset.update(status=Post.PUBLISHED)

    def make_draft(self, request, queryset):
        self.message_user(request, 'Пост снят с публикации')
        queryset.update(status=Post.DRAFT)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'joined_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_at', 'updated_at')
    list_display_links = ('id', 'content')
    search_fields = ('content',)
