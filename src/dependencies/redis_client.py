import redis.asyncio as redis

async def get_redis():
    redis_client = redis.Redis()
    try:
        yield redis_client
    finally:
        await redis_client.aclose()