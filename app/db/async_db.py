from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
print("ASYNCDBURL:", ASYNC_DATABASE_URL)

engine = create_async_engine(ASYNC_DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
