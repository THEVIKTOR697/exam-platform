from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.security import get_current_user
from app.db.sync_db import get_db
from app.models import CourseOffering

api_router = APIRouter(prefix="/offerings", tags=["Offerings"])

@api_router.get("/")
def get_offerings(db: Session = Depends(get_db), user=Depends(get_current_user)):
    offerings = db.query(CourseOffering).filter()
    return [
        {
            "id": 1,
            "title": "Certificación de Python",
            "description": "Certificación oficial de Python",
            "price": 100.0,
            "exam_id": 1
        },
        {
            "id": 2,
            "title": "Certificación de JavaScript",
            "description": "Certificación oficial de JavaScript",
            "price": 120.0,
            "exam_id": 2
        }
    ]