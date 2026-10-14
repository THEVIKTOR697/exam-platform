
import asyncio
import html
import json
import logging
import os

from datetime import datetime, timezone

import httpx
from aiokafka import AIOKafkaConsumer
from sqlalchemy.exc import IntegrityError

from app.db.sync_db import get_db_session
from app.models.purchase import Purchase
from app.models.purchase_notification import PurchaseNotification
from app.models.user import User
from app.models.certification_exam import CertificationExam
from aiokafka.errors import KafkaConnectionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOPIC = "purchase.completed"
GROUP_ID = "purchase-notification-service"
RESEND_API_URL = "https://api.resend.com/emails"


def get_notification_context(purchase_id: int):
    """Obtiene los datos de compra y registra la notificación."""

    db = get_db_session()

    try:
        purchase = (
            db.query(Purchase)
            .filter(Purchase.id == purchase_id)
            .first()
        )

        if purchase is None:
            raise ValueError(f"Purchase {purchase_id} does not exist")

        user = db.query(User).filter(
            User.id == purchase.user_id
        ).first()

        exam = db.query(CertificationExam).filter(
            CertificationExam.id == purchase.exam_id
        ).first()

        if user is None or exam is None:
            raise ValueError(
                f"Missing user or exam for purchase {purchase_id}"
            )

        notification = (
            db.query(PurchaseNotification)
            .filter(
                PurchaseNotification.purchase_id == purchase_id,
                PurchaseNotification.notification_type
                == "purchase_confirmation",
            )
            .first()
        )

        if notification is None:
            notification = PurchaseNotification(
                purchase_id=purchase_id,
                notification_type="purchase_confirmation",
                status="pending",
            )
            db.add(notification)

            try:
                db.commit()
                db.refresh(notification)
            except IntegrityError:
                # Another worker may have created this record.
                db.rollback()

                notification = (
                    db.query(PurchaseNotification)
                    .filter(
                        PurchaseNotification.purchase_id == purchase_id,
                        PurchaseNotification.notification_type
                        == "purchase_confirmation",
                    )
                    .first()
                )

                if notification is None:
                    raise

        if notification.status == "sent":
            logger.info(
                "Confirmation already sent for purchase=%s",
                purchase_id,
            )
            return None

        notification.attempt_count += 1
        notification.status = "sending"
        notification.last_error = None
        db.commit()

        return {
            "notification_id": notification.id,
            "purchase_id": purchase.id,
            "email": user.email,
            "exam_title": exam.title,
        }

    finally:
        db.close()


def update_notification(
    notification_id: int,
    status: str,
    provider_id: str | None = None,
    error: str | None = None,
):
    """Guarda el resultado del envío en PostgreSQL."""

    db = get_db_session()

    try:
        notification = (
            db.query(PurchaseNotification)
            .filter(PurchaseNotification.id == notification_id)
            .first()
        )

        if notification is None:
            raise ValueError(
                f"Notification {notification_id} does not exist"
            )

        notification.status = status
        notification.provider_id = provider_id
        notification.last_error = error

        if status == "sent":
            notification.sent_at = datetime.now(timezone.utc)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


async def send_confirmation(purchase_id: int):
    api_key = os.getenv("RESEND_API_KEY")
    email_from = os.getenv("EMAIL_FROM")
    frontend_url = os.getenv("FRONTEND_URL")

    if not api_key or not email_from or not frontend_url:
        raise RuntimeError(
            "RESEND_API_KEY, EMAIL_FROM and FRONTEND_URL are required"
        )

    context = get_notification_context(purchase_id)

    if context is None:
        return

    safe_title = html.escape(context["exam_title"])
    platform_url = f"{frontend_url.rstrip('/')}"
    safe_url = html.escape(platform_url, quote=True)

    destiny=context["email"]
    test_destiny='vmanuelnavarrete@gmail.com'
    payload = {
        "from": email_from,
        "to": [test_destiny],
        "subject": f"Confirmación de compra: {context['exam_title']}",
        "html": f"""
            <h2>¡Gracias por tu compra!</h2>
            <p>Tu compra se ha registrado correctamente.</p>
            <p><strong>Examen:</strong> {safe_title}</p>
            <p><strong>Número de compra:</strong> {context['purchase_id']}</p>
            <p>
                Puedes visitar la plataforma desde
                <a href="{safe_url}">este enlace</a>.
            </p>
        """,
        "text": (
            "¡Gracias por tu compra!\n"
            f"Examen: {context['exam_title']}\n"
            f"Número de compra: {context['purchase_id']}\n"
            f"Plataforma: {platform_url}"
        ),
    }
    logger.info(f'EMAILPAYLOAD:{payload}')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Idempotency-Key": (
            f"purchase-confirmation/{context['purchase_id']}"
        ),
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                RESEND_API_URL,
                headers=headers,
                json=payload,
            )

            if not response.is_success:
                logger.error(
                    "Resend API error: status=%s body=%s",
                    response.status_code,
                    response.text[:1000],
                )
                response.raise_for_status()

            result = response.json()

        update_notification(
            notification_id=context["notification_id"],
            status="sent",
            provider_id=result.get("id"),
        )

        logger.info(
            "Confirmation sent for purchase=%s",
            purchase_id,
        )

    except Exception as exc:
        try:
            update_notification(
                notification_id=context["notification_id"],
                status="failed",
                error=str(exc)[:2000],
            )
        except Exception:
            logger.exception(
                "Could not save notification failure for purchase=%s",
                purchase_id,
            )

        raise


async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers="kafka:9092",
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
    )

    try:
        delay = 1

        while not started:
            try:
                await consumer.start()
                started = True
                logger.info("Notification consumer started")

            except KafkaConnectionError:
                logger.exception(
                    "Kafka connection failed; retrying in %s seconds",
                    delay,
                )

                await asyncio.sleep(delay)
                delay = min(delay * 2, 30)

        async for message in consumer:
            event = json.loads(message.value.decode("utf-8"))
            purchase_id = int(event["purchase_id"])

            for attempt in range(1, 6):
                try:
                    await send_confirmation(purchase_id)

                    # Acknowledge the Kafka event only after
                    # the notification has been processed safely.
                    await consumer.commit()

                    break

                except Exception:
                    logger.exception(
                        "Attempt %s/5 failed for purchase=%s",
                        attempt,
                        purchase_id,
                    )

                    if attempt == 5:
                        # Do not commit the failed event.
                        # Let Docker restart the service so Kafka
                        # can deliver the uncommitted event again.
                        raise

                    await asyncio.sleep(min(2 ** attempt, 30))

    finally:
        if started:
            await consumer.stop()
            logger.info("Notification consumer stopped")


if __name__ == "__main__":
    asyncio.run(consume())
