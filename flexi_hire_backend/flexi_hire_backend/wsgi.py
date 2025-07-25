"""
WSGI config for flexi_hire_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flexi_hire_backend.settings')

application = get_wsgi_application()


# This file is used to configure the WSGI application for the Django project.