from django import forms
from django.core.validators import MaxLengthValidator


# insert your forms here


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
