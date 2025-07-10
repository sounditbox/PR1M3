from rest_framework import serializers

from blog.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'created_at', 'updated_at', 'author', 'post')
        read_only_fields = ('created_at', 'updated_at')


