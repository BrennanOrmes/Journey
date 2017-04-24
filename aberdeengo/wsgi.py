"""
    wsgi.py - WSGI configuration.

    Author: Team Alpha

    Tested?: Yes
    Functional?: Yes
    Merged?: Yes
    Copyright: (c) 2016, 2017 Team Alpha, University of Aberdeen.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aberdeengo.settings")

application = get_wsgi_application()

application = DjangoWhiteNoise(application)
