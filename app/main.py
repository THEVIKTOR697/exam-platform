# app/main.py
from fastapi import FastAPI, Depends
from app.db.sync_db import get_engine, get_db
from app.db.async_db import get_async_db
from app.repositories.async_repo import async_user_repository
from app.repositories.sync_repo import user_repository
from app.api.routes import router
from sqladmin import Admin, ModelView
from app.models.user import User
from app.models.exam import Exam
from starlette.middleware.sessions import SessionMiddleware
from app.auth.admin_auth import AdminAuth
import os


app = FastAPI(title="Exam Platform API")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
app.include_router(router)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
admin = Admin(app, get_engine(), authentication_backend=AdminAuth(secret_key=SECRET_KEY))

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_admin]

admin.add_view(UserAdmin)

class ExamAdmin(ModelView, model=Exam):
    column_list = [Exam.id, Exam.title, Exam.created_at]

admin.add_view(ExamAdmin)

@app.get("/")
def root():
    from app.core.config import settings
    print('SYNCDBURL: ', settings.SYNC_DATABASE_URL)
    print('ASYNC_DBURL: ', settings.ASYNC_DATABASE_URL)
    return {"message": "API running"}

@app.get("/health")
def health():
    return {"status": "ok"}
    
@app.on_event("startup")
def test_db():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            print("DB connected")
    except Exception as e:
        print("DB error:", e)
        raise e

@app.get("/sync/users")
def get_users(db=Depends(get_db)):
    return user_repository.get_users(db)

@app.get("/async/users")
async def get_users_async(db=Depends(get_async_db)):
    return await async_user_repository.get_users(db)
