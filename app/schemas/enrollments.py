from datetime import date
from pydantic import BaseModel
from typing import Optional

class EnrolBase(BaseModel):
    user_id: str
    course_id: str
    enrolled_date: date
    completed: bool = False

class Enrollment(EnrolBase):
    id: str

class EnrollmentCreate(EnrolBase):
    pass

class Response(BaseModel):
    message: str
    has_error: Optional[str] = None
    error_message: Optional[str] = None
    data: Optional[Enrollment | list[Enrollment]] = None
