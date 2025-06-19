from django.forms import forms
from django.utils.deconstruct import deconstructible


def validate_spam(value):
    if 'spam' in value:
        raise forms.ValidationError('Нельзя отправлять спам!')


@deconstructible
class CommentMaxLengthValidator:
    def __init__(self, max_length=1000):
        self.max_length = max_length

    def __call__(self, value):
        if len(value) > self.max_length:
            raise forms.ValidationError('Длина превышает 200 символов')
