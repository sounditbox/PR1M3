from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from blog.api.serializers import CommentSerializer
from blog.models import Comment


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
