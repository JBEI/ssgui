from typing import Optional

from pydantic import BaseModel, EmailStr, validator
from app.core.password_validation import PasswordValidator


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

    @validator("password")
    def password_requirements(cls, v: str) -> str:
        PasswordValidator.validate(v)
        return v


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

    @validator("password")
    def password_requirements(cls, v: Optional[str]) -> Optional[str]:
        if v:
            PasswordValidator.validate(v)
            return v
        return None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
