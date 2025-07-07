
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import RegistrationForm, ProfileEditForm
from .models import User


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


class ProfileView(DetailView):
    template_name = 'users/profile.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = User.objects.get(pk=self.kwargs['pk']).__dict__
        context['form'] = ProfileEditForm(user_data)
        return context


class ProfileEditView(UpdateView):
    template_name = 'users/profile.html'
    model = User
    form_class = ProfileEditForm
