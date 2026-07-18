from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class CertificationResult(Base):
    __tablename__ = "certification_results"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("certification_exams.id"), nullable=False)

    score = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    certification_exam = relationship(
        "CertificationExam",
        back_populates="results"
    )
