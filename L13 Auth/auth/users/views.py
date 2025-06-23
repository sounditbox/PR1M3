from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm

# Replace with built-in CBV

# def log_in(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None and user.is_active:
#             login(request, user)
#             return redirect('blog:post_list')
#     return render(request, 'users/login.html')
#
#
# @login_required
# def log_out(request):
#     logout(request)
#     return redirect('blog:post_list')


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')
