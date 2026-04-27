# app/services/task_service.py
from app.tasks.example_task import long_task

def run_long_task(x: int, y: int):
    return long_task.apply_async(args=[x, y])