import os

from celery import Celery

CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

app = Celery(
    "celery_app",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BACKEND_URL,
    include=["src.tasks.email_task"]
)

app.autodiscover_tasks()