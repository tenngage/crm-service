from fastapi import status, HTTPException
from sqlalchemy import exists, select
from src.db.base import SessionLocal
from src.models.user import User
from src.core.security import get_password_hash

async def register(db: SessionLocal, user_data):
    result = await db.execute(
        select(exists().where(User.full_name == user_data.full_name))
    )

    user_exists = result.scalar()

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user