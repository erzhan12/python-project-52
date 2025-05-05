from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Status, Label


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label=_('Статус'),
        empty_label='---------'
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_('Исполнитель'),
        empty_label='---------'
    )

    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_('Метка'),
        empty_label='---------'
    )

    self_tasks = forms.BooleanField(
        required=False,
        label=_('Только свои задачи'),
        initial=False
    )

    def clean(self):
        cleaned_data = super().clean()
        # Only validate fields if at least one filter is applied
        has_filters = any([
            cleaned_data.get('status'),
            cleaned_data.get('executor'),
            cleaned_data.get('label'),
            cleaned_data.get('self_tasks')
        ])

        if not has_filters:
            # If no filters are applied, don't validate the fields
            return cleaned_data

        # Validate status if provided
        if cleaned_data.get('status'):
            status = cleaned_data['status']
            if not Status.objects.filter(id=status.id).exists():
                self.add_error(
                    'status',
                    _('Выбранный статус не существует')
                )

        # Validate executor if provided
        if cleaned_data.get('executor'):
            executor = cleaned_data['executor']
            if not User.objects.filter(id=executor.id).exists():
                self.add_error(
                    'executor',
                    _('Выбранный исполнитель не существует')
                )

        # Validate label if provided
        if cleaned_data.get('label'):
            label = cleaned_data['label']
            if not Label.objects.filter(id=label.id).exists():
                self.add_error(
                    'label',
                    'Выбранная метка не существует'
                )

        return cleaned_data
