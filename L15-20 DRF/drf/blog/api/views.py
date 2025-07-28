from django.contrib.auth import authenticate, login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from blog.api.filters import PostFilter
from blog.api.paginations import CategoryPagination, CommentPagination, \
    PostListPagination
from blog.api.permissions import IsAuthorOrReadOnly, NoDeletePermission
from blog.api.serializers import CommentSerializer, PostSerializer, \
    CategorySerializer
from blog.models import Comment, Post, Category


# Базовый уровень - APIView
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

# Уровень 1 - generics
# class CommentDetailApiView(RetrieveUpdateDestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#
# class CommentListCreateApiView(ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     pagination_class = CommentPagination

# Уровень 2 - modelviewsets
class CommentViewSet(ModelViewSet):
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CommentPagination

    @action(detail=False, permission_classes=[IsAdminUser], methods=['delete'])
    def delete_all(self, request):
        Comment.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_all(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ModelViewSet):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [NoDeletePermission | IsAdminUser]
    pagination_class = CategoryPagination


class PostViewSet(ModelViewSet):
    model = Post
    queryset = Post.objects.all().prefetch_related('tags').select_related('category')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = PostListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['category', 'tags']
    filterset_class = PostFilter
    search_fields = ['title', 'content', 'category__title', 'tags__title', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'views']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_partial_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


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
