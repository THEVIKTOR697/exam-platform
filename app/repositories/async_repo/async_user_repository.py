# app/repositories/async/user_repository.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()
