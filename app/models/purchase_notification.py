
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.sql import func

from app.db.base import Base


class PurchaseNotification(Base):
    __tablename__ = "purchase_notifications"

    id = Column(Integer, primary_key=True)

    purchase_id = Column(
        Integer,
        ForeignKey("purchases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    notification_type = Column(
        String(50),
        nullable=False,
        default="purchase_confirmation",
    )

    status = Column(
        String(20),
        nullable=False,
        default="pending",
    )

    attempt_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    provider_id = Column(String(255), nullable=True)
    last_error = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    sent_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "purchase_id",
            "notification_type",
            name="uq_purchase_notification_type",
        ),
    )
