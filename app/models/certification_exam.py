from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class CertificationExam(Base):
    __tablename__ = "certification_exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    institution_id = Column(ForeignKey("institutions.id"), nullable=False)
    course_id = Column(ForeignKey("certification_courses.id"), nullable=True)

    results = relationship(
        "CertificationResult",
        back_populates="certification_exam"
    )

    institution = relationship(
        "Institution",
        back_populates="certification_exams"
    )

    certification_course = relationship(
        "CertificationCourse",
        back_populates="certification_exam"
    )

    questions = relationship(
        "Question",
        back_populates="exam",
        cascade="all, delete-orphan"
    )
