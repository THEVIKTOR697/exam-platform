import stripe
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import os

from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.sync_db import get_db
from app.models import Purchase

api_router = APIRouter(prefix="/payments", tags=["payments"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

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
        success_url=f"{os.getenv('FRONTEND_URL')}/success?exam_id={data.exam_id}",
        cancel_url=f"{os.getenv('FRONTEND_URL')}/cancel",
        metadata={
            "user_id": str(user.id),
            "exam_id": str(data.exam_id),
        }
    )

    return {"url": session.url}

from fastapi import Request, HTTPException

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

    print("EVENTOOOOO:", event)
    # PAGO COMPLETADO
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("STRIPESESSION:", session)
        print("METADATA:", session.metadata)

        metadata = dict(session.metadata) if session.metadata else {}

        user_id = metadata.get("user_id")
        exam_id = metadata.get("exam_id")

        if session["payment_status"] != "paid":
            return

        if not user_id or not exam_id:
            print("⚠️ Metadata missing (normal in stripe trigger)")
            return {"status": "ignored"}

        user_id = int(user_id)
        exam_id = int(exam_id)

        existing = db.query(Purchase).filter_by(
            user_id=user_id,
            exam_id=exam_id
        ).first()

        if not existing:
            purchase = Purchase(
                user_id=user_id,
                exam_id=exam_id
            )
            db.add(purchase)
            db.commit()

        print(f"Compra guardada: user {user_id}, exam {exam_id}")

    return {"status": "page.tsx"}
