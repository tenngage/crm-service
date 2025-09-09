from fastapi import APIRouter, Depends
from typing import Annotated
from src.dependencies.current_user import get_current_user
from src.schemas.user_schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[
        UserResponse, Depends(get_current_user)
    ]
):
    return current_user