from fastapi import APIRouter, Depends
from typing import Annotated
from src.db.base import SessionLocal
from src.dependencies.current_user import get_current_user
from src.dependencies.session import get_db
from src.schemas.user_schemas import UserResponse, UserRegister
from src.crud.register import register

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register")
async def register_new_user(
    user_data: UserRegister,
    db: SessionLocal = Depends(get_db)
):
    return await register(db, user_data)

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[
        UserResponse, Depends(get_current_user)
    ]
):
    return current_user