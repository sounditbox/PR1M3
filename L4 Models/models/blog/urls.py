from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.post_list, name="post_list"),
    path("posts/<int:id>/", views.post_detail, name="post_detail"),
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/<int:id>/update", views.update_post, name="update_post"),
    path("posts/<int:id>/delete", views.delete_post, name="delete_post"),
]
