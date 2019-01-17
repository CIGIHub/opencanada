"""
WSGI config for opencanada project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('OPEN_CANADA_PYTHON_ENV') == 'staging':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opencanada.settings.staging')
elif os.environ.get('OPEN_CANADA_PYTHON_ENV') == 'admin':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opencanada.settings.admin'))
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opencanada.settings.production')

application = get_wsgi_application()
