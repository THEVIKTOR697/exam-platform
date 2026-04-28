# app/models/exam.py

from sqlalchemy import Column, Integer, String, Date
from app.db.base import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    created_at = Column(Date)