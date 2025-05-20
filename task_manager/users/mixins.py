from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


class CheckUser(UserPassesTestMixin):
    def test_func(self):
        user = self.get_object()
        if user == self.request.user:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = gettext(
            "user can be delete or update only user which created"
        )
        self.permission_denied_url = reverse_lazy("users:list")
        return super().dispatch(request, *args, **kwargs)


class NoPermissionHandleMixin:
    permission_denied_message = ""
    permission_denied_url = reverse_lazy("users:list")

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_denied_url)