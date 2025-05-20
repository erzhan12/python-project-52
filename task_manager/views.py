from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.forms import CustomLoginForm


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login_form.html'
    form_class = CustomLoginForm
    next_page = reverse_lazy('index')
    success_message = _('You were logged in')


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You were logged out'))
        return super().dispatch(request, *args, **kwargs)
