from fastapi import APIRouter
from app.tasks.example_task import long_task
from app.core.celery_app import celery
from app.tasks.report_task import generate_users_report
from fastapi.responses import FileResponse
import os

api_router = APIRouter()

@api_router.post("/test-task")
def test_task():
    task = long_task.delay(2, 3)
    return {
        "task_id": task.id,
        "status": "submitted"
    }


@api_router.get("/task/{task_id}")
def get_task(task_id: str):
    result = celery.AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }

@api_router.post("/reports/users")
def create_report():
    task = generate_users_report.delay()

    return {
        "task_id": task.id,
        "status": "processing"
    }


@api_router.get("/reports/{task_id}")
def get_report_status(task_id: str):
    result = celery.AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": result.status,
    }

    if result.status == "PROGRESS":
        response["progress"] = result.info

    if result.status == "SUCCESS":
        response["result"] = result.result

    if result.status == "FAILURE":
        response["error"] = str(result.result)

    return response


@api_router.get("/reports/download/{task_id}")
def download_report(task_id: str):
    file_path = f"reports/report_{task_id}.csv"

    if not os.path.exists(file_path):
        return {"error": "File missing on API container."}

    return FileResponse(file_path, filename="users_report.csv")