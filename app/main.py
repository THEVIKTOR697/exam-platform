# app/main.py

from fastapi import FastAPI

app = FastAPI(title="Exam Platform API")

@app.get("/")
def root():
    return {"message": "API running"}