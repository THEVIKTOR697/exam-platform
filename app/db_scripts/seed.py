# seed.py

from app.db.sync_db import get_db
from app.models.user import User
from app.auth.security import hash_password

db = next(get_db())

users = [
    User(
    name="admin",
    email="admin@test.com",
    password_hash=hash_password("admin123"),
    is_admin=True
    ),
    User(
    name="Frodo",
    email="frodo@shire.com",
    password_hash=hash_password("pass123"),
    is_admin=False
    ),
    User(
    name="Sam",
    email="sam@shire.com",
    password_hash=hash_password("pass123"),
    is_admin=False
    ), 
    User(
    name="Gandalf",
    email="gandalf@middleearth.com",
    password_hash=hash_password("pass123"),
    is_admin=False
    )
]

db.add_all(users)
db.commit()