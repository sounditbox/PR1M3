from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentApiView, PostApiView

app_name = 'api'

router = DefaultRouter()
router.register('comments', CommentApiView)
router.register('posts', PostApiView)


urlpatterns = [
    # path('comments/', CommentApiView.as_view(), name='comments'),
    # path('comments/<int:id>', CommentApiView.as_view(), name='comment'),
    path('', include(router.urls))
]
