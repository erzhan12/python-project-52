from django.forms import ModelForm

from task_manager.mixins import FormStyleMixin
from task_manager.statuses.models import Status


class StatusCreationForm(FormStyleMixin, ModelForm):
    class Meta:
        model = Status
        fields = ['name']