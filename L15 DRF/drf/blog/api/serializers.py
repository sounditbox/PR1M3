from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import StringRelatedField, PrimaryKeyRelatedField

from blog.models import Category, Comment, Tag, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = ('id',)

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Title is too short')
        return value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    post = StringRelatedField()

    class Meta:
        model = Comment
        fields = ('content', 'created_at', 'updated_at', 'author', 'post')
        read_only_fields = ('created_at', 'updated_at', 'author', 'post')


class PostSerializer(serializers.ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'content', 'created_at', 'updated_at', 'category',
                  'tags', 'comments', 'author')
        read_only_fields = ('created_at', 'updated_at', 'category', 'tags', 'comments')

    def create(self, validated_data):
        validated_data['author'] = get_user_model().objects.first()
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        queryset = Post.objects.all()
        fields = ('id', 'title', 'author')
