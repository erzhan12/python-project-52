from django.contrib import admin

from .models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ['name', 'created_at']
    list_filter = ['created_at']


admin.site.register(Status, StatusAdmin)