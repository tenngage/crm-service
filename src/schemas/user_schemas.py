from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserInDB(UserBase):
    hashed_password: str


class UserResponse(UserBase):
    id: int


class UserRegister(UserBase):
    password: str
