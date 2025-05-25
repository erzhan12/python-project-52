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
)
from task_manager.statuses.forms import StatusCreationForm
from task_manager.statuses.models import Status

URL_INDEX = 'statuses:index'


class StatusListView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    template_name = 'statuses/status_form.html'
    form_class = StatusCreationForm
    success_url = reverse_lazy(URL_INDEX)
    success_message = _('Status was created successfully')
    extra_context = {
        'title': _('Create status'),
        'button_name': _('Create')
    }


class StatusUpdateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    form_class = StatusCreationForm
    model = Status
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy(URL_INDEX)
    success_message = _('Status was updated successfully')
    extra_context = {
        'title': _('Update status'),
        'button_name': _('Update')
    }


class StatusDeleteView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       ProtectErrorMixin,
                       DeleteView):
    template_name = 'statuses/status_delete.html'
    model = Status
    success_url = reverse_lazy(URL_INDEX)
    success_message = _('Status was deleted successfully')
    protected_object_url = reverse_lazy(URL_INDEX)
    protected_object_message = _(
        'Cannot delete this status because they are being used'
    )
    extra_context = {
        'title': _('Status deletion'),
        'button_name': _('Yes, delete')
    }