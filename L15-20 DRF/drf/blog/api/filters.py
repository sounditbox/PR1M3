from django_filters import DateFilter
from django_filters.rest_framework import FilterSet

from blog.models import Post


class PostFilter(FilterSet):
    created_before = DateFilter(field_name='created_at', lookup_expr='lt')
    created_after = DateFilter(field_name='created_at', lookup_expr='gt')

    class Meta:
        model = Post
        fields = ['category', 'tags', 'created_before', 'created_after', 'created_at', 'author__username']
