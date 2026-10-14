# app/kafka/outbox_worker.py

import asyncio
import logging
from datetime import datetime, timezone

from app.db.sync_db import get_session_local
from app.models import OutboxEvent
from app.kafka.producer import KafkaProducer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

POLL_INTERVAL = 1
BATCH_SIZE = 100


async def process_outbox():
    log.info("OUTBOX WORKER: starting")

    SessionLocal = get_session_local()
    producer = await start_producer_with_retry()

    try:
        while True:
            try:
                # Get pending event IDs using a short-lived session.
                with SessionLocal() as db:
                    event_ids = [
                        event_id
                        for (event_id,) in (
                            db.query(OutboxEvent.id)
                            .filter(OutboxEvent.status == "pending")
                            .order_by(OutboxEvent.created_at)
                            .limit(BATCH_SIZE)
                            .all()
                        )
                    ]

                if event_ids:
                    log.info(
                        "OUTBOX WORKER: found %s pending events",
                        len(event_ids),
                    )

                for event_id in event_ids:
                    try:
                        # Load each event in its own session.
                        with SessionLocal() as db:
                            event = db.get(OutboxEvent, event_id)

                            if event is None or event.status != "pending":
                                continue

                            topic = event.event_type
                            payload = event.payload

                            # Publish before marking the event as published.
                            await producer.send(topic, payload)

                            event.status = "published"
                            event.published_at = datetime.now(timezone.utc)
                            event.last_error = None
                            db.commit()

                            log.info(
                                "OUTBOX WORKER: published event_id=%s topic=%s",
                                event_id,
                                topic,
                            )

                    except Exception as exc:
                        # Record the failure without losing the pending event.
                        log.exception(
                            "OUTBOX WORKER: failed event_id=%s",
                            event_id,
                        )

                        try:
                            with SessionLocal() as db:
                                event = db.get(OutboxEvent, event_id)

                                if event is not None and event.status == "pending":
                                    event.retry_count += 1
                                    event.last_error = str(exc)[:2000]
                                    db.commit()
                        except Exception:
                            log.exception(
                                "OUTBOX WORKER: could not record failure "
                                "for event_id=%s",
                                event_id,
                            )

            except Exception:
                log.exception("OUTBOX WORKER: polling failed")

            await asyncio.sleep(POLL_INTERVAL)

    finally:
        await producer.stop()

async def start_producer_with_retry():
    delay = 1

    while True:
        producer = KafkaProducer()

        try:
            await producer.start()
            log.info("OUTBOX WORKER: Kafka producer connected")
            return producer

        except Exception:
            log.exception(
                "OUTBOX WORKER: Kafka connection failed; "
                "retrying in %s seconds",
                delay,
            )

            try:
                await producer.stop()
            except Exception:
                log.debug(
                    "OUTBOX WORKER: producer cleanup failed",
                    exc_info=True,
                )

            await asyncio.sleep(delay)
            delay = min(delay * 2, 30)


if __name__ == "__main__":
    asyncio.run(process_outbox())