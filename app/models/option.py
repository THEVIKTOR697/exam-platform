from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from app.db.base import Base


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)