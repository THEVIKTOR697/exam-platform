#exams/schemas.py
from pydantic import BaseModel
from typing import List


# ---------- Requests ----------
class Answer(BaseModel):
    question_id: int
    selected_option: int

class SubmitExamRequest(BaseModel):
    exam_id: int
    answers: List[Answer]


# ---------- Responses ----------
class ExamResponse(BaseModel):
    id: int
    title: str
    price: float

    class Config:
        from_attributes = True
