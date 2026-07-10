from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.sync_db import get_db
from app.exams.schemas import SubmitExamRequest
from app.models import Result
from app.models.question import Question
from app.models.option import Option
from app.models.purchase import Purchase
from app.auth.security import get_current_user

api_router = APIRouter(prefix="/exams", tags=["Exams"])

@api_router.get("/")
def get_exams():
    return [
        {"id": 1, "title": "Matemáticas Básicas", "price": 10},
        {"id": 2, "title": "Programacion Básica", "price": 10},
    ]

@api_router.get("/{exam_id}/questions")
def get_exam_questions(exam_id: int, db: Session = Depends(get_db)):
    questions = db.query(Question).filter_by(exam_id=exam_id).all()

    result = []

    for q in questions:
        options = db.query(Option).filter_by(question_id=q.id).all()

        result.append({
            "question_id": q.id,
            "text": q.text,
            "options": [
                {
                    "id": o.id,
                    "text": o.text
                } for o in options
            ]
        })

    return result

@api_router.get("/{exam_id}/access")
def check_access(
    exam_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    purchase = db.query(Purchase).filter_by(
        user_id=user.id,
        exam_id=exam_id
    ).first()

    return {"has_access": purchase is not None}


@api_router.post("/submit-exam")
def submit_exam(
    data: SubmitExamRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    questions = db.query(Question).filter_by(exam_id=data.exam_id).all()
    if not questions:
        return {"error": "Examen sin preguntas"}

    correct_map = {}

    for q in questions:
        correct_option = next(
            (opt.id for opt in q.options if opt.is_correct),
            None
        )
        correct_map[q.id] = correct_option

    total_questions = len(correct_map)

    if len(data.answers) < total_questions:
        return {"error": "Debes responder todas las preguntas"}

    correct_count = 0

    for answer in data.answers:
        correct = correct_map.get(answer.question_id)

        if correct is not None and answer.selected_option == correct:
            correct_count += 1

    score = (correct_count / total_questions) * 100

    # 🎯 5. Definir aprobado/reprobado
    passed = score >= 70

    # 💾 6. Guardar resultado
    result = Result(
        user_id=user.id,
        exam_id=data.exam_id,
        score=score,
        passed=passed,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    # 📤 7. Respuesta
    return {
        "score": score,
        "passed": passed,
        "correct_answers": correct_count,
        "total_questions": total_questions,
    }


#     # Validar compra
#     purchase = db.query(Purchase).filter_by(
#         user_id=user.id,
#         exam_id=data.exam_id
#     ).first()
#
#     if not purchase:
#         raise HTTPException(status_code=403, detail="No has comprado este examen")
#
    # # Evitar múltiples intentos
    # existing_result = db.query(Result).filter_by(
    #     user_id=user.id,
    #     exam_id=data.exam_id
    # ).first()
    #
    # if existing_result:
    #     raise HTTPException(status_code=400, detail="Ya presentaste este examen")

    # 🧠 3. Obtener preguntas reales (AQUÍ debes conectar tu modelo)
    # 🔥 EJEMPLO SIMULADO (reemplaza con DB real)
