import os
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from src.schemas.token_schemas import TokenData
from src.models.user import User
from src.core.exceptions import CredentialsException

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str,
):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(
    token: str,
    db: AsyncSession,
    redis_client: redis.Redis,
) -> dict:
    try:
        blacklist_check = await redis_client.get(f"blacklist:{token}")
        if blacklist_check:
            raise CredentialsException()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise CredentialsException()
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise CredentialsException()
    stmt = select(User).where(User.username == token_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise CredentialsException()
    return user


def get_token_ttl(token: str) -> int:

    # Checking if the token has expired
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False}
        )
        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            return 0

        # Returning remaining time
        remaining = exp_timestamp - datetime.now(timezone.utc).timestamp()
        return max(0, int(remaining))

    # Returning 0 if token has expired
    except InvalidTokenError:
        return 0
