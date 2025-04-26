from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import init_db
from app.db.redis import init_redis
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.roles import router as roles_router

app = FastAPI()

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'larni qo'shish
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)

# Startup va shutdown eventlari
@app.on_event("startup")
async def startup_event():
    await init_db(app)
    await init_redis(app)

@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, "redis"):
        await app.state.redis.close()