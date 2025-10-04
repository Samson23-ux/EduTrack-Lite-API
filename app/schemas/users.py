from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True

class User(UserBase):
    id: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    current_password: str

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class Response(BaseModel):
    message: str
    has_error: Optional[str] = None
    error_message: Optional[str] = None
    data: Optional[User | list[User]] = None
