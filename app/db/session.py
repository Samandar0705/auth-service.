from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Asinxron engine yaratish
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Asinxron sessiya factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session