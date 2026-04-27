# app/tasks/example_task.py
from celery import shared_task
import time

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def long_task(self, x: int, y: int):
    print(f"[Celery] Processing {x} + {y}")
    time.sleep(5)
    return x + y
