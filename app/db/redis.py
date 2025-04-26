import redis.asyncio as redis
from app.core.config import settings
from fastapi import FastAPI, Request

async def init_redis(app: FastAPI) -> None:
    app.state.redis = redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True
    )

async def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis