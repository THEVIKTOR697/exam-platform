from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.sync_db import get_db
from app.auth.security import get_current_user
from app.models.certification_result import CertificationResult

api_router = APIRouter(prefix="/results", tags=["Results"])

@api_router.get("/")
def get_results(db: Session = Depends(get_db), user=Depends(get_current_user)):
    results = db.query(CertificationResult).filter(CertificationResult.user_id == user.id).all()

    return {
        "results": [
            {
                "title": r.exam.title,
                "score": r.score,
                "passed": r.passed,
                "created_at": r.created_at.strftime("%d/%m/%Y %H:%M hrs"),
            }
            for r in results
        ]
    }
