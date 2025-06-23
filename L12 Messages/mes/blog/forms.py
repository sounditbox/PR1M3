from django import forms
from django.core.validators import MaxLengthValidator

from .models import Post, Comment
from .validators import validate_spam


class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Как вас зовут?'}
                           ),
                           validators=[MaxLengthValidator(50)]
                           )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}),
        error_messages={
            'required': 'Поле обязательно для заполнения',
            'invalid': 'Введите корректный email!'
        }
    )

    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Напишите ваш вопрос'}))

    agree = forms.BooleanField(
        initial=True,
        label="Согласен с условиями",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    def clean_message(self):
        message = self.cleaned_data['message']
        if 'spam' in message:
            self.add_error('message', 'Нельзя отправлять спам!')
        return message

    def clean_name(self):
        name = self.cleaned_data['name']
        if 'spam' in name:
            raise forms.ValidationError('Нельзя отправлять спам!')
        return name


class PostForm(forms.ModelForm):
    extra = forms.CharField(required=False, validators=[validate_spam])

    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'status', 'author', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Содержимое'}),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=Post.STATUS_CHOICES),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'title': {
                'required': 'Поле обязательно для заполнения',
                'max_length': 'Длина превышает 200 символов',
            },
            'content': {
                'required': 'Поле обязательно для заполнения',
            },
            'status': {
                'required': 'Поле обязательно для заполнения',
            },
            'author': {
                'required': 'Поле обязательно для заполнения',
            },
            'category': {
                'required': 'Поле обязательно для заполнения',
            }
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержимое',
            'status': 'Статус',
            'author': 'Автор',
            'category': 'Категория',
            'image': 'Изображение',
        }
        help_texts = {
            'title': 'Введите заголовок поста',
            'content': 'Введите содержимое поста',
            'status': 'Выберите статус поста',
            'author': 'Выберите автора поста',
            'category': 'Выберите категорию поста',
            'image': 'Выберите изображение',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if 'spam' in title:
            raise forms.ValidationError('Нельзя отправлять спам!')
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if 'spam' in content:
            raise forms.ValidationError('Нельзя отправлять спам!')
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
        }
        labels = {
            'content': 'Комментарий'
        }
        error_messages = {
            'content': {
                'required': 'Поле обязательно для заполнения',
            },
        }
