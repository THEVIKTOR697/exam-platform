from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("certification_exams.id"), nullable=False)
    text = Column(String, nullable=False)

    options = relationship("Option", back_populates="question")

    exam = relationship(
        "CertificationExam",
        back_populates="questions"
    )