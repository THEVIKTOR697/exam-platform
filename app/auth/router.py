from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sync_db import get_db
from app.models.user import User
from .schemas import RegisterSchema, LoginSchema, TokenResponse
from .service import create_user, authenticate_user
from .security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    user = create_user(db, data.email, data.password)
    return {"message": "Usuario creado"}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token}