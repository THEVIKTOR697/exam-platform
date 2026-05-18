# security.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.sync_db import get_db
from app.models.user import User
import os

TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        valid = ph.verify(hashed, password)

        if ph.check_needs_rehash(hashed):
            return "rehash"

        return valid
    except VerifyMismatchError:
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),  # issued at
    })

    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[ALGORITHM])

        #user_id: int = payload.get("user_id")
        user_id = payload.get("sub")
        user_name = payload.get("email")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user
