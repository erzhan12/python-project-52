from django.db import models
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        verbose_name=_('Name'),
        unique=True,
        error_messages={
            'unique': _('This label with this name already exists. '
                        'Please choose another name.'),
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.task_set.exists():
            raise ProtectedError(
                _("Cannot delete this label because they are being used"),
                self
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')