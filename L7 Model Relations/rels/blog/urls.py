from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/<int:id>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/create/", views.CreatePostView.as_view(), name="create_post"),
    path("posts/<int:id>/update/", views.UpdatePostView.as_view(), name="post_edit"),
    path("posts/<int:pk>/delete/", views.DeletePostView.as_view(), name="post_delete"),
    path('posts/<int:post_id>/comment/', views.create_comment, name='comment_create'),
    path('example/', views.SimpleView.as_view(), name='example'),
]
