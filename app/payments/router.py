import stripe
import os
import logging
from fastapi import APIRouter, Depends, Request, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth.security import get_current_user
from app.db.sync_db import get_db
from app.models import Purchase

api_router = APIRouter(prefix="/payments", tags=["Payments"])
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
log = logging.getLogger(__name__)


class CheckoutRequest(BaseModel):
    exam_id: int
    title: str
    price: int  # en USD


@api_router.post("/create-checkout-session")
def create_checkout_session(
        data: CheckoutRequest,
        user=Depends(get_current_user)
):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "mxn",
                "product_data": {
                    "name": data.title,
                },
                "unit_amount": data.price * 100,
            },
            "quantity": 1,
        }],
        # success_url=f"{os.getenv('FRONTEND_URL')}/success?exam_id={data.exam_id}",
        success_url=f"{os.getenv('FRONTEND_URL')}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{os.getenv('FRONTEND_URL')}/cancel",
        metadata={
            "user_id": str(user.id),
            "exam_id": str(data.exam_id),
        }
    )

    return {"url": session.url}


@api_router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    log.info(f"EEEEEEEEEEEEEEEEEVNTO: {event}")
    # PAGO COMPLETADO
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"].to_dict()
        log.info(f"Checkout session: {session}")
        if session.get("payment_status") != "paid":
            return

        metadata = session.get("metadata", {}) or {}
        user_id = metadata.get("user_id")
        exam_id = metadata.get("exam_id")

        if not user_id or not exam_id:
            log.info("Metadata missing")
            return {"status": "ignored"}

        user_id = int(user_id)
        exam_id = int(exam_id)

        # PROD
        # existing = db.query(Purchase).filter_by(
        #     stripe_session_id=session.get("id")
        # ).first()
        existing = db.query(Purchase).filter_by(
            user_id=user_id,
            exam_id=exam_id
        ).first()

        if not existing:
            purchase = Purchase(
                user_id=user_id,
                exam_id=exam_id,
                stripe_session_id=session.get("id"),
                payment_intent_id=session.get("payment_intent"),
                amount=session.get("amount_total"),
                currency=session.get("currency"),
                status="paid"
            )
            log.info(f"ENV: {os.getenv('ENV')}")
            try:
                log.info('Adding payment to user')
                db.add(purchase)
                db.flush()
                db.commit()
            except IntegrityError:
                db.rollback()
                if os.getenv("ENV") == "development":
                    log.info("⚠️ Duplicate allowed in dev")
                else:
                    raise

        log.info(f"Compra guardada: user {user_id}, exam {exam_id}")

    return {"status": "page.tsx"}


@api_router.get("/verify-session")
def verify_session(
        session_id: str = Query(...),
        db: Session = Depends(get_db)
):
    log.info(f"VERIFYYINNNNG: {session_id}")
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session_id")

    try:
        stripe_session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session_id")

    session = stripe_session.to_dict()
    metadata = session.get("metadata", {}) or {}
    user_id=metadata.get("user_id")
    exam_id=metadata.get("exam_id")

    if not metadata.get("user_id"):
        raise HTTPException(status_code=400, detail="Invalid session metadata")

    if session.get("payment_status") != "paid":
        raise HTTPException(status_code=400, detail="Payment not completed")

    # PROD
    # purchase = db.query(Purchase).filter_by(
    #     stripe_session_id=session_id
    # ).first()

    purchase = db.query(Purchase).filter_by(
        user_id=user_id,
        exam_id=exam_id
    ).first()

    if not purchase:
        # ⚠️ webhook aún no llegó (Stripe puede tardar unos segundos)
        raise HTTPException(
            status_code=404,
            detail="Purchase not found yet, try again"
        )

    return {
        "status": "success",
        "exam_id": purchase.exam_id
    }
