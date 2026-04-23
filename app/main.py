# app/main.py

from fastapi import FastAPI, Depends
from app.db.sync_db import get_engine, get_db
from app.db.async_db import get_async_db
from app.repositories.async_repo import async_user_repository
from app.repositories.sync_repo import user_repository

app = FastAPI(title="Exam Platform API")

@app.get("/")
def root():
    from app.core.config import settings
    print('DBURL: ', settings.SYNC_DATABASE_URL)
    print('DBURL: ', settings.ASYNC_DATABASE_URL)
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
    