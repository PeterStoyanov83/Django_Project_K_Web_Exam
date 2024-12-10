import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_k.settings')

app = Celery('project_k')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'rpc://')

CELERY_BROKER_URL = 'pyamqp://guest@localhost//'