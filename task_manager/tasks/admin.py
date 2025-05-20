from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'author',
                    'executor', 'created_at', 'get_labels')
    search_fields = ['name', 'description', 'author', 'executor']
    list_filter = ['status', 'author', 'executor', 'labels', 'created_at']
    filter_horizontal = ('labels',)
    ordering = ('-created_at',)

    @admin.display(description='Labels')
    def get_labels(self, obj):
        return ', '.join([label.name for label in obj.labels.all()])


admin.site.register(Task, TaskAdmin)