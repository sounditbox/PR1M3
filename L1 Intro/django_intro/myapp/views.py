from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import MyModel


def show_models(request: HttpRequest) -> HttpResponse:
    all_models = MyModel.objects.all()
    context = {'models': all_models, 'title': 'Мои модели'}
    return render(request, 'index.html', context)
