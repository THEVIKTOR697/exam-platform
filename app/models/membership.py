from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.db.base import Base

class Membership(Base):
    __tablename__ = "memberships"
    __table_args__ = (
        UniqueConstraint("user_id", "institution_id", "role_id"),
    )

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    user = relationship("User", backref="memberships")
    institution = relationship("Institution", backref="memberships")
    role = relationship("Role", backref="memberships")

    Index("ix_membership_user", "user_id"),
    Index("ix_membership_institution", "institution_id"),
