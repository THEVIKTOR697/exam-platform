from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grade_id = Column(ForeignKey("grades.id"))
    description = Column(String, nullable=True)
    code = Column(String, unique=True, nullable=False)
    credits = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())
    institution_id = Column(
        Integer,
        ForeignKey("institutions.id"),
        nullable=False
    )

    offerings = relationship(
        "CourseOffering",
        back_populates="subject",
        cascade="all, delete-orphan"
    )
    institution = relationship("Institution", back_populates="subjects")
