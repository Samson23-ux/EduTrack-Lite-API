from pydantic import BaseModel
from typing import Optional
from app.schemas.users import User

class CourseBase(BaseModel):
    title: str
    description: str
    is_open: bool = True

class Course(CourseBase):
    id: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_open: Optional[bool] = None

class Response(BaseModel):
    message: str
    has_error: Optional[str] = None
    error_message: Optional[str] = None
    data: Optional[Course | list[Course] | list[User]] = None
