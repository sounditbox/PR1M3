
from django.urls import path
from .views import show_models

urlpatterns = [
    path('', show_models)
]
