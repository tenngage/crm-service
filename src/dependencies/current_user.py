from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from src.core.security import oauth2_scheme, decode_token
from src.dependencies.session import get_db
from src.dependencies.redis_client import get_redis
from src.models.user import User
from src.core.exceptions import InactiveUserException


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
    redis_client: Annotated[redis.Redis, Depends(get_redis)]
):
    return await decode_token(token, db, redis_client)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user
