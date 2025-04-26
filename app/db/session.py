from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from fastapi import FastAPI

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db(app: FastAPI) -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # Jadvalarni o'chirish (faol qilishdan oldin ehtiyot bo'ling)
        # await conn.run_sync(Base.metadata.create_all)  # Jadvalarni yaratish
        pass

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session