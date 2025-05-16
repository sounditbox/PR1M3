from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .models import MyModel


def show_all_models(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            name = 'Untitled'
        desc = request.POST.get('description')
        if not desc:
            desc = 'No description'
        MyModel.objects.create(name=name, description=desc)
        return redirect('myapp:models')
    all_models = MyModel.objects.all()
    context = {'models': all_models, 'title': 'Мои модели'}
    return render(request, 'myapp/models.html', context)


def show_one_model(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'GET':
        model = MyModel.objects.get(id=id)
        context = {'model': model, 'title': model.name}
        return render(request, 'myapp/one_model.html', context)
    elif request.method == 'POST':
        model = MyModel.objects.get(id=id)
        model.name = request.POST.get('name', model.name)
        model.description = request.POST.get('description', model.description)
        model.save()
        return redirect('myapp:one_model', id)


def delete_model(request: HttpRequest, id: int) -> HttpResponse:
    model = MyModel.objects.get(id=id)
    model.delete()
    return redirect('myapp:models')


def index(request: HttpRequest) -> HttpResponse:
    class A:
        def __init__(self):
            self.a = 1

        def b(self):
            return 2

        def __str__(self):
            return 'A'

    context = {
        'title': 'Главная',
        'list': [1, 2, 3],
        'dict': {'a': 1, 'b': 2},
        'a': A(),
    }
    return render(request, 'myapp/index.html', context)


def home(request: HttpRequest) -> HttpResponse:
    return redirect('myapp:index')
