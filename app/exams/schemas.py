from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    question_id: int
    selected_option: int

class SubmitExamRequest(BaseModel):
    exam_id: int
    answers: List[Answer]
