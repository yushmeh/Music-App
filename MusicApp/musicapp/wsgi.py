import os
import django
from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musicapp.settings")
django.setup()
application = WSGIHandler()