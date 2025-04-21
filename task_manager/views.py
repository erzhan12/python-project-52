# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
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
from .models import Status, Task, Label
from .forms import TaskFilterForm
from django.db.models import ProtectedError


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
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_func(self):
        # Проверяем, совпадает ли id пользователя с id профиля
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        # Сообщение при отказе в доступе
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.login_required_msg)
            return redirect(self.login_url)
        else:
            no_perm_ms = _('У вас нет прав для изменения другого пользователя')
            messages.error(self.request, no_perm_ms)
            # Redirect to users list for authenticated users without permission
            return redirect(reverse_lazy('users'))


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, DeleteView):
    """Delete user account."""
    model = User
    template_name = 'task_manager/user_confirm_delete.html'
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно удален')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_func(self):
        # Проверяем, совпадает ли id пользователя с id профиля
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        # Сообщение при отказе в доступе
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.login_required_msg)
            return redirect(self.login_url)
        else:
            no_perm_msg = _('У вас нет прав для удаления другого пользователя')
            messages.error(self.request, no_perm_msg)
            return redirect(reverse_lazy('users'))

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        tasks = Task.objects.filter(created_by=user)
        if tasks.exists():
            messages.error(
                request,
                _('Невозможно удалить пользователя, потому что он используется')
            )
            return redirect(reverse_lazy('users'))
        return super().post(request, *args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    """Custom form for user registration with additional fields."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username']


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


class UserLoginView(SuccessMessageMixin, LoginView):
    """Handle user login."""
    template_name = 'task_manager/login.html'
    next_page = reverse_lazy('index')
    redirect_authenticated_user = True
    extra_context = {
        'title': _('Вход'),
        'button_text': _('Войти')
    }
    success_message = _('Вы залогинены')

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
            messages.info(request, _('Вы разлогинены'))
        return redirect('index')


class StatusListView(LoginRequiredMixin, ListView):
    """Display list of all statuses."""
    model = Status
    template_name = 'task_manager/statuses_list.html'
    context_object_name = 'statuses'
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_queryset(self):
        return Status.objects.all()

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Handle status creation."""
    model = Status
    template_name = 'task_manager/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('statuses')
    success_message = _('Статус успешно создан')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Создать статус')
        context['button_text'] = _('Создать')
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Handle status update."""
    model = Status
    template_name = 'task_manager/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('statuses')
    success_message = _('Статус успешно изменен')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменение статуса')
        context['button_text'] = _('Изменить')
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Handle status deletion."""
    model = Status
    template_name = 'task_manager/status_confirm_delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Статус успешно удален')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_manager/tasks_list.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskFilterForm(self.request.GET)

        if form.is_valid():
            filter_conditions = {}

            if form.cleaned_data.get('status'):
                filter_conditions['status'] = form.cleaned_data['status']

            if form.cleaned_data.get('executor'):
                filter_conditions['executor'] = form.cleaned_data['executor']

            if form.cleaned_data.get('label'):
                filter_conditions['labels'] = form.cleaned_data['label']

            if form.cleaned_data.get('self_tasks'):
                filter_conditions['created_by'] = self.request.user

            if filter_conditions:
                queryset = queryset.filter(**filter_conditions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Handle Task Creation"""
    model = Task
    template_name = 'task_manager/task_form.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks')
    success_message = _('Задача успешно создана')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Handle Task Update"""
    model = Task
    template_name = 'task_manager/task_form.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks')
    success_message = _('Задача успешно изменена')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменение задачи')
        context['button_text'] = _('Изменить')
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """Handle Task Deletion"""
    model = Task
    template_name = 'task_manager/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Задача успешно удалена')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_func(self):
        # Проверяем, является ли текущий пользователь автором задачи
        task = self.get_object()
        return self.request.user == task.created_by

    def handle_no_permission(self):
        # Сообщение при отказе в доступе
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.login_required_msg)
            return redirect(self.login_url)
        else:
            no_perm_msg = _('Задачу может удалить только её автор')
            messages.error(self.request, no_perm_msg)
            return redirect(reverse_lazy('tasks'))


class TaskDetailView(LoginRequiredMixin, DetailView):
    """Handle Task Detail View"""
    model = Task
    template_name = 'task_manager/task_detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)
