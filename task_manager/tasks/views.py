from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import AuthorPermissionMixin, CustomLoginRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.models import Task


class TaskListView(CustomLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    ordering = 'id'


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task was created successfully')
    extra_context = {
        'title': _('Create task'),
        'button_name': _('Create')
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task was updated successfully')
    extra_context = {
        'button_name': _('Update'),
        'title': _('Update task')
    }


class TaskDeleteView(CustomLoginRequiredMixin,
                     AuthorPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task was deleted successfully')
    permission_denied_url = reverse_lazy('tasks:index')
    permission_denied_message = _("Only the task's author can delete it")
    extra_context = {
        'title': _('Task deletion'),
        'button_name': _('Yes, delete')
    }