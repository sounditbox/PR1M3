from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Никнейм')
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(
                                  attrs={'class': 'form-control'}),
                              label='Аватар'
                              )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль ещё раз')

    class Meta:
        model = User
        fields = ('email', 'avatar', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует')
        return email


class LogInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name')
