# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def index(request):
    """Render the index page."""
    return render(request, "task_manager/index.html")


class UserListView(ListView):
    """Display list of all users."""
    model = User
    template_name = 'task_manager/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, UpdateView):
    """Update user information."""
    model = User
    template_name = 'task_manager/user_form.html'
    fields = ['first_name', 'last_name', 'username']
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно изменен')

    def test_func(self):
        # Проверяем, совпадает ли id пользователя с id профиля
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        # Сообщение при отказе в доступе
        messages.error(self.request,
                       _('У вас нет прав для изменения другого пользователя'))
        return redirect('users')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, DeleteView):
    """Delete user account."""
    model = User
    template_name = 'task_manager/user_confirm_delete.html'
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно удален')

    def test_func(self):
        # Проверяем, совпадает ли id пользователя с id профиля
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        # Сообщение при отказе в доступе
        messages.error(self.request,
                       _('У вас нет прав для удаления другого пользователя'))
        return redirect('users')


class CustomUserCreationForm(UserCreationForm):
    """Custom form for user registration with additional fields."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UserCreateView(SuccessMessageMixin, CreateView):
    """Handle user registration."""
    form_class = CustomUserCreationForm
    template_name = 'task_manager/user_registration_form.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно создан')

    def form_valid(self, form):
        """Handle form validation with password warning support."""
        try:
            return super().form_valid(form)
        except ValidationError as e:
            if any('warning' in getattr(err, 'code', '')
                    for err in e.error_list):
                return super().form_valid(form)
            raise


class UserLoginView(LoginView):
    """Handle user authentication."""
    template_name = 'task_manager/login.html'
    next_page = reverse_lazy('index')
    redirect_authenticated_user = True
    extra_context = {
        'title': _('Вход'),
        'button_text': _('Войти')
    }

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            print("User is authenticated")
            messages.info(request, _('Вы уже авторизованы'))
            return redirect('index')
        return super().get(request, *args, **kwargs)


class UserLogoutView(LoginView):
    """Handle user logout."""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, _('Вы вышли из системы'))
        return redirect('index')
