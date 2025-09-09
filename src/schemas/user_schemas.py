from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True
