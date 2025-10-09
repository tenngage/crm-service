from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from src.dependencies.current_user import get_current_user
from src.dependencies.session import get_db
from src.dependencies.redis_client import get_redis
from src.services.user_services import register, login, logout
from src.schemas.user_schemas import (
    UserResponse,
    UserRegister
)
from src.schemas.token_schemas import Token
from src.core.security import security, oauth2_scheme
from src.tasks.email_task import send_email

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register_new_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    result = await register(db, user_data)
    print(result.email)

    try:
        task = send_email.delay(
            user_email=result.email,
            username=result.username,
        )
        print("Task successfully created")

    except Exception as e:
        print(f"Error during sending welcome email: {e}")

    return result


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends()
    ],
    db: AsyncSession = Depends(get_db),
) -> Token:
    return await login(form_data, db)


@router.post("/logout")
async def logout_from_system(
    token: Annotated[
        str,
        Depends(oauth2_scheme)
    ],
    redis_client: Annotated[
        redis.Redis,
        Depends(get_redis)
    ]
):
    return await logout(token, redis_client)


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[
        UserResponse, Depends(get_current_user)
    ]
):
    return current_user
