from app.models.institution import Institution
from app.models.certification_exam import CertificationExam
from app.db.sync_db import get_session_local

SessionLocal = get_session_local()

def seed_exams():
    db = SessionLocal()
    try:
        with SessionLocal.begin() as db:
            institutions = db.query(Institution).all()
            exam1 = CertificationExam(
                institution_id=institutions[0].id,
                title="Python Básico",
                description="Evaluación de fundamentos de Python",
                price=1.99,
                is_active=True
            )

            exam2 = CertificationExam(
                institution_id=institutions[1].id,
                title="Matemáticas Básicas",
                description="Evaluación de conocimientos matemáticos",
                price=1.99,
                is_active=True
            )

            db.add_all([exam1, exam2])
        return exam1, exam2
    finally:
        db.close()

if __name__ == "__main__":
    seed_exams()
