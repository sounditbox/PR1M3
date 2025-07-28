from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Для получения пары токенов по username/password
    TokenRefreshView,  # Для обновления Access токена с помощью Refresh токена
)

from .views import CommentViewSet, PostViewSet, SessionAuthView, TokenAuthView, \
    CategoryViewSet

app_name = 'api'

router = DefaultRouter()
router.register('comments', CommentViewSet)
router.register('posts', PostViewSet)
router.register('categories', CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('session_auth/', SessionAuthView.as_view()),
    path('token_auth/', TokenAuthView.as_view()),

    path('jwt_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt_token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

]
