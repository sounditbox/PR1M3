from rest_framework.pagination import PageNumberPagination, \
    LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class PostListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class CategoryPagination(LimitOffsetPagination):
    limit_query_param = 'l'
    offset_query_param = 'o'
    default_limit = 2
    max_limit = 5


class CommentPagination(CursorPagination):
    ordering = '-created_at'
    page_size = 2
