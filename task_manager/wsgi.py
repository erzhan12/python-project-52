"""
WSGI config for task_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

print(100 * "=")
print(os.system('ls task_manager'))
print(100 * "=")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()
