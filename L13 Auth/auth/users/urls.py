from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .forms import LogInForm


app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        form_class=LogInForm
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
