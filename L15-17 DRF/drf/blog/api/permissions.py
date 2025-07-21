from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from blog.models import Comment, Post


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request: Request, view,
                              obj: Comment | Post):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user


class NoDeletePermission(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method != 'DELETE'
