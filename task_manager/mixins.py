from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class FormStyleMixin:
    """Adds Bootstrap styles to form fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_input_class = (
            'form-control bg-secondary bg-opacity-50 border-secondary'
        )
        base_select_class = (
            'form-select bg-secondary bg-opacity-50 border-secondary'
        )

        for name, field in self.fields.items():
            attrs = {
                'placeholder': field.label
            }

            if name == 'description':
                attrs['class'] = base_input_class
                attrs['rows'] = '3'
            elif name in ['status', 'executor']:
                attrs['class'] = base_select_class
            else:
                attrs['class'] = base_input_class

            field.widget.attrs.update(attrs)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Redirects unauthorized users without showing extra messages."""
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            msg = _('You are not authorized! Please, log in.')
            messages.error(self.request, msg)
        return super().handle_no_permission()


class BasePermissionMixin(UserPassesTestMixin):
    """Base mixin for object permission checks."""
    permission_denied_url = reverse_lazy('users:index')
    permission_denied_message = _('Permission denied')
    redirect_field_name = None

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.permission_denied_url)
        return super().handle_no_permission()


class UserPermissionMixin(BasePermissionMixin):
    """Allows access only to the profile owner."""
    msg = _('You do not have permission to change another user.')
    permission_denied_message = msg

    def test_func(self):
        return self.get_object() == self.request.user


class AuthorPermissionMixin(BasePermissionMixin):
    """Allows access only to the object author."""
    msg = _('You do not have permission to change this object.')
    permission_denied_message = msg

    def test_func(self):
        return self.get_object().author == self.request.user


class ProtectErrorMixin:
    """Handles ProtectedError exceptions on object deletion."""
    protected_object_message = _(
        'Cannot delete object because it is being used.'
    )
    protected_object_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_object_message)
            return redirect(self.protected_object_url)