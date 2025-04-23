from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Имя'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Имя'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Имя')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Описание')
    )
    status = models.ForeignKey(
        "Status",
        on_delete=models.CASCADE,
        verbose_name=_('Статус'),
        related_name="tasks"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_by',
        verbose_name=_('Автор')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('Исполнитель'),
        null=True,
        blank=True
    )
    labels = models.ManyToManyField(
        Label,
        related_name="tasks",
        verbose_name=_('Метки'),
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
