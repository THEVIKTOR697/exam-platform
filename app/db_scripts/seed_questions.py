# seed_questions.py
from app.models import CertificationExam
from app.models.question import Question
from app.models.option import Option
from app.db.sync_db import get_db_session

db = get_db_session()

def seed_questions():
    exams = db.query(CertificationExam).all()
    if not exams:
        print("No exams found. Please seed exams first.")
        return
    e1=exams[0]
    e2=exams[0]

    q1 = Question(exam_id=e1.id, text="¿Qué es Python?")
    db.add(q1)
    db.flush()

    options1 = [
        Option(question_id=q1.id, text="Lenguaje de programación", is_correct=True),
        Option(question_id=q1.id, text="Base de datos", is_correct=False),
        Option(question_id=q1.id, text="Sistema operativo", is_correct=False),
    ]

    q2 = Question(exam_id=e1.id, text="¿Qué son los tipos de datos mutables e inmutables?")
    db.add(q2)
    db.flush()

    options2 = [
        Option(question_id=q2.id, text="Los objetos mutables (listas, diccionarios) pueden cambiar tras su creación, mientras que los inmutables (cadenas, tuplas, números) no.", is_correct=True),
        Option(question_id=q2.id, text="Un programa de television", is_correct=False),
        Option(question_id=q2.id, text="Son datos estadisticos financieros", is_correct=False),
    ]

    q3 = Question(exam_id=e1.id, text="Diferencia entre Lista y Tupla")
    db.add(q3)
    db.flush()

    options3 = [
        Option(question_id=q3.id, text="Las listas [] son mutables (se pueden cambiar) y las tuplas () son inmutables (no se pueden cambiar)", is_correct=True),
        Option(question_id=q3.id, text="Las listas consumen menos memoria", is_correct=False),
        Option(question_id=q3.id, text="Una tupla se puede modificar despues de su creacion", is_correct=False),
    ]

    q4 = Question(exam_id=e2.id, text="¿Cual es la raiz cuadrada de 144?")
    db.add(q4)
    db.flush()

    options4 = [
        Option(question_id=q4.id, text="12", is_correct=True),
        Option(question_id=q4.id, text="500", is_correct=False),
        Option(question_id=q4.id, text="60", is_correct=False),
    ]

    q5 = Question(exam_id=e2.id, text="¿Cuanto vale pi(\(\pi \))?")
    db.add(q5)
    db.flush()

    options5 = [
        Option(question_id=q5.id, text="3.141519", is_correct=True),
        Option(question_id=q5.id, text="90", is_correct=False),
        Option(question_id=q5.id, text="0", is_correct=False),
    ]

    q6 = Question(exam_id=e2.id, text="Que es un Axioma?")
    db.add(q6)
    db.flush()

    options6 = [
        Option(question_id=q6.id, text="Una proposición evidente por sí misma que no necesita demostración, sirviendo de base.", is_correct=True),
        Option(question_id=q6.id, text="Una parte del cuerpo", is_correct=False),
        Option(question_id=q6.id, text="Una bebida energetica", is_correct=False),
    ]

    all_options = [
        *options1,
        *options2,
        *options3,
        *options4,
        *options5,
        *options6,
    ]

    db.add_all(all_options)
    db.commit()
    db.close()


if __name__ == "__main__":
    seed_questions()
