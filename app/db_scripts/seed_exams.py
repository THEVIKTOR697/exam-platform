from app.models.certification_exam import CertificationExam
from app.db.sync_db import get_session_local

SessionLocal = get_session_local()

def seed_exams():
    db = SessionLocal()

    exam1 = CertificationExam(
        institution_id=1,
        title="Python Básico",
        description="Evaluación de fundamentos de Python",
        price=1.99,
        is_active=True
    )

    exam2 = CertificationExam(
        institution_id=2,
        title="Matemáticas Básicas",
        description="Evaluación de conocimientos matemáticos",
        price=1.99,
        is_active=True
    )

    db.add_all([exam1, exam2])
    db.commit()
    db.close()

    return exam1, exam2

if __name__ == "__main__":
    seed_exams()
