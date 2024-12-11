import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_k.settings')

app = Celery('project_k')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Use Redis as the broker and result backend
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'django://')
app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'django-db')

# Retry connection on startup
app.conf.broker_connection_retry_on_startup = True
