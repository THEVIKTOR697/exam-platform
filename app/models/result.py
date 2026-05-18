from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)

    score = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())