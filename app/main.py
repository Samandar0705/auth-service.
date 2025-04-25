from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router


app = FastAPI(
    title="Authentication & Authorization Microservice",
    description="A microservice for handling authentication and authorization",
    version="1.0.0",
)

# CORS sozlamalari (frontend uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Productionda aniq domenlarni kiriting
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth router'ni qo'shish
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Authentication & Authorization Microservice"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"users": [{"id": user.id, "email": user.email} for user in users]}