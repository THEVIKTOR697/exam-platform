
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Text, func
from app.db.base import Base
from sqlalchemy.dialects.postgresql import JSONB

class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(
        BigInteger,
        primary_key=True,
    )

    aggregate_type = Column(
        String(100),
        nullable=False,
    )

    aggregate_id = Column(
        String(100),
        nullable=False,
    )

    event_type = Column(
        String(150),
        nullable=False,
    )

    payload = Column(
        JSONB,
        nullable=False,
    )

    status = Column(
        String(20),
        nullable=False,
        server_default="pending",
    )

    retry_count = Column(
        Integer,
        nullable=False,
        server_default="0",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    published_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_error = Column(
        Text,
        nullable=True,
    )
