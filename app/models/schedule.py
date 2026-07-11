from sqlalchemy import Column, Integer, ForeignKey, String, Time
from sqlalchemy.orm import relationship
from app.db.base import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)

    offering_id = Column(Integer, ForeignKey("course_offerings.id"), nullable=False)

    # 0=Lun, 1=Mar, 2=Mie...
    day_of_week = Column(Integer, nullable=False)

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    classroom = Column(String, nullable=True)

    offering = relationship("CourseOffering", back_populates="schedules")
