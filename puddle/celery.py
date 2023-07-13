from celery import Celery

app = Celery('puddle')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()