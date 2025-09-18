from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from src.dependencies.current_user import get_current_user
from src.dependencies.session import get_db
from src.services.user_services import register, login
from src.schemas.user_schemas import (
    UserResponse,
    UserRegister
)
from src.schemas.token_schemas import Token

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register_new_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    return await register(db, user_data)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm, Depends()
    ],
    db: AsyncSession = Depends(get_db),
) -> Token:
    return await login(form_data, db)


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[
        UserResponse, Depends(get_current_user)
    ]
):
    return current_user
