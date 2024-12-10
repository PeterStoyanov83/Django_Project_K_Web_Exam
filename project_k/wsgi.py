import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_k.settings')

print("Loading WSGI application...")

sys.stdout.flush()
application = get_wsgi_application()

print("WSGI application loaded.")
sys.stdout.flush()
