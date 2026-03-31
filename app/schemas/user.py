from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True