from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Enrollment(Base):

    __tablename__ = "enrollments"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "offering_id",
            name="uq_student_offering"
        ),
    )

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    offering_id = Column(Integer, ForeignKey("course_offerings.id"), nullable=False)
    status = Column(String, default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    dropped_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="enrollments")
    offering = relationship("CourseOffering", back_populates="enrollments")
