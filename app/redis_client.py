# app/redis_client.py
from redis.asyncio import Redis
from app.config import REDIS_HOST, REDIS_PORT

redis: Redis = None

async def init_redis():
    global redis
    redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def close_redis():
    await redis.close()

def get_redis() -> Redis:
    return redis
