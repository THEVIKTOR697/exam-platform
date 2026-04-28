# admin_auth.py
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from sqlalchemy.orm import Session
from app.db.sync_db import get_db_session
from app.models.user import User
from app.auth.security import verify_password

class AdminAuth(AuthenticationBackend):

    def __init__(self, secret_key: str):
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        db: Session = get_db_session()

        user = db.query(User).filter(User.email == email).first()

        if user and user.is_admin and verify_password(password, user.password_hash):
            request.session.update({"admin_id": user.id})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "admin_id" in request.session
    