from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class CourseOffering(Base):
    __tablename__ = "course_offerings"

    id = Column(Integer, primary_key=True)

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)

    # "Grupo A", "Grupo B"
    group = Column(String, nullable=True)

    capacity = Column(Integer, nullable=True)

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    subject = relationship("Subject", back_populates="offerings")
    schedules = relationship("Schedule", back_populates="offering")
    offering = relationship("CourseOffering", back_populates="enrollments")
