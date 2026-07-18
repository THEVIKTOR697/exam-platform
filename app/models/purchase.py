from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Numeric, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    exam_id = Column(
        Integer,
        ForeignKey("certification_exams.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 💳 Stripe
    stripe_session_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    payment_intent_id = Column(
        String,
        unique=True,
        nullable=True
    )

    amount = Column(Numeric(10, 2), nullable=False)

    currency = Column(
        String(10),
        nullable=False,
        default="usd"
    )

    status = Column(
        String(20),
        nullable=False,
        default="pending"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "exam_id", name="uq_user_exam_purchase"),
    )
