from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str

    class Config:
        from_attributes = True