from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    membership_id = Column(Integer, ForeignKey("memberships.id"), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    student_number = Column(String, unique=True, nullable=False)
    current_grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    enrollments = relationship("Enrollment", back_populates="student")
    membership = relationship("Membership", back_populates="student")
