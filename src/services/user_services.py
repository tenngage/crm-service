from datetime import timedelta

from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.token_schemas import Token
from src.models.user import User
from src.core.exceptions import WrongCredentialsException
from src.core.security import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


async def register(db: AsyncSession, user_data):

    # Check if username already exists
    username_exists = await db.execute(
        select(exists().where(User.username == user_data.username))
    )
    if username_exists.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    email_exists = await db.execute(
        select(exists().where(User.email == user_data.email))
    )

    if email_exists.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hashing password
    hashed_password = get_password_hash(user_data.password)

    # Creating db_user object for inserting into db
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )

    # Inserting into db with commit
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def login(
    form_data: OAuth2PasswordRequestForm,
    db: AsyncSession
):
    # Authenticating user
    user = await authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise WrongCredentialsException()

    # Creating access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
