from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import oauth2_scheme, decode_token
from src.dependencies.session import get_db
from src.models.user import User
from src.core.exceptions import InactiveUserException


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await decode_token(token, db)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user
