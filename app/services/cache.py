# app/services/cache.py
from app.redis_client import get_redis

async def get_cached_status(url: str) -> str | None:
    redis = get_redis()
    return await redis.get(url)

async def cache_url_status(url: str, status: str):
    redis = get_redis()
    await redis.setex(url, 50, status)
