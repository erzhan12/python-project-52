from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.mixins import (
    CustomLoginRequiredMixin,
    ProtectErrorMixin,
    UserPermissionMixin,
)
from task_manager.users.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from task_manager.users.models import User

URL_INDEX = 'users:index'
ERROR_MESSAGE_NO_RIGHTS = _("You don't have rights to change another user.")


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']


class BaseUserView(SuccessMessageMixin):
    model = User
    template_name = 'users/registration_form.html'
    context_object_name = 'user'
    permission_denied_url = reverse_lazy('users:index')


class UserCreateView(BaseUserView, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    success_message = _('User was registered successfully')
    extra_context = {
        'title': _('Sign Up'),
        'button_name': _('Register')
    }


class UserUpdateView(CustomLoginRequiredMixin, UserPermissionMixin,
                     BaseUserView, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy(URL_INDEX)
    success_message = _('User was updated successfully')
    permission_denied_message = ERROR_MESSAGE_NO_RIGHTS
    extra_context = {
        'title': _('Edit profile'),
        'button_name': _('Save changes')
    }


class UserDeleteView(CustomLoginRequiredMixin, UserPermissionMixin,
                     ProtectErrorMixin, BaseUserView, DeleteView):
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy(URL_INDEX)
    success_message = _('User was deleted successfully')
    permission_denied_message = ERROR_MESSAGE_NO_RIGHTS
    access_denied_message = ERROR_MESSAGE_NO_RIGHTS
    protected_object_url = reverse_lazy(URL_INDEX)
    protected_object_message = _(
        'Cannot delete this user because they are being used'
    )
    extra_context = {
        'title': _('User deletion'),
        'button_name': _('Yes, delete')
    }