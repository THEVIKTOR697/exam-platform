# app/repositories/sync/user_repository.py
from app.models.user import User

def get_users(db):
    return db.query(User).all()
