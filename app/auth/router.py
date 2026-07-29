from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sync_db import get_db
from app.models.user import User
from .schemas import RegisterSchema, LoginSchema, TokenResponse
from .service import create_user, authenticate_user
from .security import create_access_token
from app.auth.security import get_current_user


api_router = APIRouter(prefix="/auth", tags=["Auth"])


@api_router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    print(data.dict())
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    user = create_user(db, data.name, data.email, data.password)
    return {"message": "Usuario creado"}


@api_router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    print('LOOOOOOOOOOOOOOOOOOOGIIIIIIIIIN')
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({
        "user_id": str(user.id),
        "email": user.email
    })

    return {"access_token": token}

@api_router.get("/me")
def get_current_student_data(user=Depends(get_current_user)):

    student_membership = next(
        (m for m in user.memberships if m.role.name == "student"),
        None
    )

    if not student_membership:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "institution": None,
        }

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "institution": student_membership.institution.name,
    }
