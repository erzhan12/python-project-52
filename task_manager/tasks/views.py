# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView
from django.views.generic import DeleteView, CreateView, DetailView
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


def index(request):
    """Render the index page."""
    return render(request, "tasks/index.html")


class UserListView(ListView):
    """Display list of all users."""
    model = User
    template_name = 'tasks/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


class UserUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    """Update user information."""
    model = User
    template_name = 'tasks/user_form.html'
    fields = ['first_name', 'last_name', 'username']
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно изменен')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _(
        'Вы не авторизованы! Пожалуйста, выполните вход.'
    )

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


class UserDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    """Delete user account."""
    model = User
    template_name = 'tasks/user_confirm_delete.html'
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно удален')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _(
        'Вы не авторизованы! Пожалуйста, выполните вход.'
    )
    user_used_msg = _(
        'Невозможно удалить пользователя, потому что он используется'
    )

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
                self.user_used_msg
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
    template_name = 'tasks/user_registration_form.html'
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
    template_name = 'tasks/login.html'
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
    template_name = 'tasks/statuses_list.html'
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
    template_name = 'tasks/status_form.html'
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
    template_name = 'tasks/status_form.html'
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
    template_name = 'tasks/status_confirm_delete.html'
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
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskFilterForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['executor']:
                queryset = queryset.filter(executor=form.cleaned_data['executor'])
            if form.cleaned_data['label']:
                queryset = queryset.filter(labels=form.cleaned_data['label'])
            if form.cleaned_data['self_tasks']:
                queryset = queryset.filter(created_by=self.request.user)

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
    template_name = 'tasks/task_form.html'
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
    template_name = 'tasks/task_form.html'
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


class TaskDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    """Handle Task Deletion"""
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Задача успешно удалена')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _(
        'Вы не авторизованы! Пожалуйста, выполните вход.'
    )

    def test_func(self):
        # Проверяем, является ли текущий пользователь автором задачи
        return self.get_object().created_by == self.request.user

    def handle_no_permission(self):
        # Сообщение при отказе в доступе
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.login_required_msg)
            return redirect(self.login_url)
        else:
            no_perm_msg = _('Задачу может удалить только ее автор')
            messages.error(self.request, no_perm_msg)
            return redirect(reverse_lazy('tasks'))


class TaskDetailView(LoginRequiredMixin, DetailView):
    """Handle Task Detail View"""
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'tasks/labels_list.html'
    context_object_name = 'labels'
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_queryset(self):
        return Label.objects.all()

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Handle label creation."""
    model = Label
    template_name = 'tasks/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('labels')
    success_message = _('Метка успешно создана')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Создать метку')
        context['button_text'] = _('Создать')
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Handle label update."""
    model = Label
    template_name = 'tasks/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('labels')
    success_message = _('Метка успешно изменена')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменение метки')
        context['button_text'] = _('Изменить')
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)


class LabelDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    """Handle label deletion."""
    model = Label
    template_name = 'tasks/label_confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _('Метка успешно удалена')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    login_required_msg = _(
        'Вы не авторизованы! Пожалуйста, выполните вход.'
    )
    label_used_msg = _('Невозможно удалить метку, потому что она используется')

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        # Check if any tasks are using this label
        if Task.objects.filter(labels=label).exists():
            messages.error(request, self.label_used_msg)
            return redirect(reverse_lazy('labels'))
        return super().post(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, self.login_required_msg)
        return redirect(self.login_url)
