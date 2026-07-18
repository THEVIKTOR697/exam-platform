# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)

    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    memberships = relationship(
        "Membership",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    enrollments = relationship("Enrolment",
                              back_populates="user",
                              cascade="all, delete-orphan")
