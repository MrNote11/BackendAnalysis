"""Celery app: reads CELERY_* settings from Django and finds each app's tasks.py."""
from celery import Celery

from config.env import setup_settings_module

setup_settings_module()

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
