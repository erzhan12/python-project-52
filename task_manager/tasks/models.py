from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
        verbose_name=_('Name'),
        error_messages={
            'unique': _('This task with this name already exists. '
                        'Please choose another name.'),
        }
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='author',
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
    )
    executor = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        related_name='executor',
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_('Labels'),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')