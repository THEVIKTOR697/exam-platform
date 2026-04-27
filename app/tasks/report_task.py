from celery import shared_task
import csv
import os
import time

OUTPUT_DIR = "/app/reports"

@shared_task(bind=True)
def generate_users_report(self):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_path = os.path.join(OUTPUT_DIR, f"report_{self.request.id}.csv")

    # Simulación de datos reales (aquí iría DB)
    users = [
        {"id": 1, "name": "Alice", "email": "alice@test.com"},
        {"id": 2, "name": "Bob", "email": "bob@test.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@test.com"},
    ]

    # Simular proceso pesado
    for i in range(5):
        time.sleep(1)
        self.update_state(state="PROGRESS", meta={"step": i + 1})

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "name", "email"])
        writer.writeheader()
        writer.writerows(users)
    #return {"file_url": "https://s3.amazonaws.com/..."}
    return {"file_path": file_path}
