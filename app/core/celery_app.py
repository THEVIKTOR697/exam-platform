# app/core/celery_app.py
from celery import Celery
import app.tasks.example_task
import app.tasks.report_task
import os
import sys

sys.path.append(os.getcwd())

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery = Celery(
    "exam-platform",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
)

celery.autodiscover_tasks(["app.tasks"])


celery.conf.update(
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
)