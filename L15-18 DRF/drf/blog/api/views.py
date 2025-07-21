from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from blog.api.permissions import IsAuthorOrReadOnly, NoDeletePermission
from blog.api.serializers import CommentSerializer, PostSerializer, \
    CategorySerializer
from blog.models import Comment, Post, Category


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


class CategoryViewSet(ModelViewSet):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [NoDeletePermission | IsAdminUser]


class CommentViewSet(ModelViewSet):
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]


class PostViewSet(ModelViewSet):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SessionAuthView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'status': 'error', 'message': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {'status': 'error', 'message': 'Email or password invalid'},
                status=status.HTTP_400_BAD_REQUEST)
        # SessionID in cookie
        login(request, user)
        return Response({'status': 'success'})


class TokenAuthView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'status': 'error', 'message': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {'status': 'error', 'message': 'Email or password invalid'},
                status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'status': 'success', 'token': token.key})
