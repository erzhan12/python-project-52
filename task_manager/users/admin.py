from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_joined')
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['date_joined']


admin.site.register(User, UserAdmin)