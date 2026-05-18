from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.sync_db import get_db
from app.auth.security import get_current_user
from app.models.result import Result

api_router = APIRouter(prefix="/results", tags=["Results"])

@api_router.get("/")
def get_results(db: Session = Depends(get_db), user=Depends(get_current_user)):
    results = db.query(Result).filter(Result.user_id == user.id).all()

    return {
        "results": [
            {
                "title": r.exam.title,
                "score": r.score,
                "passed": r.passed,
            }
            for r in results
        ]
    }
