from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from blog.api.serializers import CommentSerializer, PostSerializer
from blog.models import Comment, Post


# class CommentApiView(APIView):
#     def get(self, request, *args, **kwargs):
#         if 'id' in kwargs:
#             comments = Comment.objects.get(id=kwargs['id'])
#         else:
#             comments = Comment.objects.all()
#         serializer = CommentSerializer(comments, many=not 'id' in kwargs)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

class CommentApiView(ModelViewSet):
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostApiView(ModelViewSet):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
