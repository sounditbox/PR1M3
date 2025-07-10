from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentApiView

app_name = 'api'

router = DefaultRouter()
router.register('comments', CommentApiView, basename='comments')

urlpatterns = [
    # path('comments/', CommentApiView.as_view(), name='comments'),
    # path('comments/<int:id>', CommentApiView.as_view(), name='comment'),
    path('', include(router.urls))
]
