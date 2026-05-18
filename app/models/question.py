from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)

    text = Column(String, nullable=False)