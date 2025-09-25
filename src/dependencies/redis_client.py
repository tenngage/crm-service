import os

import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

async def get_redis():
    redis_client = redis.Redis.from_url(REDIS_URL)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()