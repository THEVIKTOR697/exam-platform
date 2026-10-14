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
from app.models import OutboxEvent

api_router = APIRouter(prefix="/payments", tags=["Payments"])
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class CheckoutRequest(BaseModel):
    exam_id: int
    title: str
    price: int  # en USD
    checkout_request_id: str


@api_router.post("/create-checkout-session")
def create_checkout_session(
        data: CheckoutRequest,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    purchase = db.query(Purchase).filter_by(
        user_id=user.id,
        checkout_request_id=data.checkout_request_id,
    ).first()

    if not purchase:
        # IMPORTANT: in production, obtain the price and title
        # from your database, not from client-supplied values.
        purchase = Purchase(
            user_id=user.id,
            exam_id=data.exam_id,
            checkout_request_id=data.checkout_request_id,
            amount=data.price * 100, # CHECK FIX
            currency="mxn",
            status="pending",
        )

        try:
            db.add(purchase)
            db.commit()
            db.refresh(purchase)

        except IntegrityError:
            # Another concurrent request may have created it.
            db.rollback()
            purchase = db.query(Purchase).filter_by(
                user_id=user.id,
                checkout_request_id=data.checkout_request_id,
            ).first()
            if not purchase:
                raise HTTPException(
                    status_code=500,
                    detail="Could not recover checkout order",
                )

    # Never create another Checkout for an already-paid order.
    if purchase.status == "paid":
        raise HTTPException(
            status_code=409,
            detail="This purchase has already been completed",
        )

    # 2. If a Stripe session was saved, reuse it.
    if purchase.stripe_session_id:
        existing_session = stripe.checkout.Session.retrieve(
            purchase.stripe_session_id
        )

        if existing_session.status == "open":
            return {"url": existing_session.url}

        if existing_session.status == "complete":
            raise HTTPException(
                status_code=409,
                detail="Checkout is complete; payment is being reconciled",
            )

        # Do not silently create a new payable session here.
        raise HTTPException(
            status_code=409,
            detail="Checkout session is no longer open; reconcile its payment status before retrying",
        )
    # 3. Create/recover Stripe Checkout using a stable key.
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "mxn",
                    "product_data": {
                        "name": data.title,
                    },
                    "unit_amount": int(purchase.amount * 100),
                },
                "quantity": 1,
            }],
            # success_url=f"{os.getenv('FRONTEND_URL')}/success?exam_id={data.exam_id}",
            success_url=f"{os.getenv('FRONTEND_URL')}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/cancel",
            metadata={
                "purchase_id": str(purchase.id),
                "user_id": str(user.id),
                "exam_id": str(purchase.exam_id),
            },
            idempotency_key=f"purchase-{purchase.id}-checkout",
        )
    except stripe.error.StripeError:
        # Keep the persisted order pending. A retry must reuse
        # this same purchase ID and Stripe idempotency key.
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail="Unable to create Checkout session; retry the same operation",
        )

    # 4. Persist the Stripe session ID.
    try:
        purchase.stripe_session_id = session.id
        db.commit()
    except Exception:
        db.rollback()
        # Stripe may have created the session successfully.
        # A retry uses the same idempotency key and recovers it.
        raise HTTPException(
            status_code=503,
            detail="Checkout created but not yet saved; retry the same operation",
        )

    return {"url": session.url}


@api_router.post("/webhook")
async def stripe_webhook(
        request: Request,
        db: Session = Depends(get_db)
    ):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except ValueError as e:
        log.exception("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        log.exception("Invalid Stripe signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    # PAGO COMPLETADO
    log.info(f"WEBHOOK PAGO COMPLETADO: {event}")

    event_type = event["type"]
    # Ignore unrelated events.
    if event_type != "checkout.session.completed":
        return {"status": "ignored"}

    session = event["data"]["object"].to_dict()
    log.info(f"WEBHOOK Session: {session}")
    # Validate the payment before granting access
    if session.get("payment_status") != "paid":
        raise HTTPException(status_code=400, detail="Payment not completed")

    metadata = session.get("metadata", {}) or {}
    user_id = metadata.get("user_id")
    exam_id = metadata.get("exam_id")
    purchase_id = metadata.get("purchase_id")
    session_id = session.get("id")

    if not all([user_id, exam_id, purchase_id, session_id]):
        log.error("Required Stripe metadata is missing")
        raise HTTPException(
            status_code=400,
            detail="Missing required metadata",
        )

    try:
        user_id = int(user_id)
        exam_id = int(exam_id)
        purchase_id = int(purchase_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid purchase metadata",
        )

    try:
        # Lock the order to serialize concurrent webhook deliveries.
        purchase = (
            db.query(Purchase)
            .filter(
                Purchase.id == purchase_id,
                Purchase.user_id == user_id,
                Purchase.exam_id == exam_id,
            )
            .with_for_update()
            .first()
        )

        log.info(f"ENV: {os.getenv('ENV')}")
        if not purchase:
            # A transient failure should be retried by Stripe.
            raise HTTPException(
                status_code=500,
                detail="Purchase order not found",
            )

        # Never associate a different Stripe session with this order.
        if purchase.stripe_session_id != session_id:
            raise HTTPException(
                status_code=400,
                detail="Stripe session does not match purchase",
            )

        # Idempotency: a repeated webhook must not create
        # another purchase.completed outbox event.
        if purchase.status == "paid":
            log.info(
                "Purchase %s already processed",
                purchase.id,
            )
            return {"status": "already_processed"}

        # Update the existing persistent order.
        purchase.payment_intent_id = session.get(
            "payment_intent"
        )
        purchase.amount = session.get("amount_total")
        purchase.currency = session.get("currency")
        purchase.status = "paid"

        # Store the event in the same database transaction.
        outbox_event = OutboxEvent(
            aggregate_type="purchase",
            aggregate_id=str(purchase.id),
            event_type="purchase.completed",
            payload={
                "purchase_id": purchase.id,
                "user_id": purchase.user_id,
                "exam_id": purchase.exam_id,
                "stripe_session_id": session_id,
                "payment_intent_id": session.get("payment_intent"),
                "amount": session.get("amount_total"),
                "currency": session.get("currency"),
            },
        )
        db.add(outbox_event)
        db.commit()
        log.info(f"Purchase {purchase.id}  marked paid; outbox event stored, {purchase.id}")
        log.info(f"Compra guardada: user {user_id}, exam {exam_id}")
        return {
            "status": "success",
            "purchase_id": purchase.id,
        }
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        log.exception(
            "Integrity error processing purchase %s",
            purchase_id,
        )
        raise HTTPException(
            status_code=500,
            detail="Could not process purchase",
        )
    except Exception:
        db.rollback()
        log.exception(
            "Unexpected error processing purchase %s",
            purchase_id,
        )
        raise HTTPException(
            status_code=500,
            detail="Could not process payment",
        )

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
            status_code=202,
            detail="Purchase not found yet, webhook may not respond yet , try again"
        )

    return {
        "status": "success",
        "exam_id": purchase.exam_id
    }
