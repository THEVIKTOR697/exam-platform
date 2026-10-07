from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.security import get_current_user
from app.db.sync_db import get_db
from app.models import CourseOffering

api_router = APIRouter(prefix="/course_offerings", tags=["Offerings"])

@api_router.get("/")
def get_offerings(db: Session = Depends(get_db)):

    course_offerings = db.query(CourseOffering).all()
    offerings = [
        {
            "id": offering.id,
            "institution_id": offering.institution_id,
            "capacity": offering.capacity,
            "subject": offering.subject.name,
            "teacher": offering.teacher.user.name,
            "start_time": offering.start_time,
            "end_time": offering.end_time,
            "group_name": offering.group_name,
        }
        for offering in course_offerings
    ]

    return offerings
