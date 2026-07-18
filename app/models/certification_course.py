from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class CertificationCourse(Base):
    __tablename__ = "certification_courses"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    description = Column(String)

    institution_id = Column(ForeignKey("institutions.id"), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    institution = relationship("Institution")
    certification_exam = relationship("CertificationExam", back_populates="certification_course")
