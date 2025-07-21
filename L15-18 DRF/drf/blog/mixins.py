from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin


class MessageHandlerFormMixin(FormMixin):
    success_message = 'Success!'
    error_message = 'Something went wrong...'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class IsAuthorMixin(SingleObjectMixin):
    def dispatch(self, request, *args, **kwargs):
        to_handle = self.get_object()
        if to_handle.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)