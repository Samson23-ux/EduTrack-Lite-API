from fastapi import Request
from fastapi.responses import JSONResponse

#errors
class UserExistError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class PasswordError(Exception):
    pass

class CourseExistError(Exception):
    pass

class CourseNotFoundError(Exception):
    pass

class EnrollmentNotFoundError(Exception):
    pass

class EnrollmentExistError(Exception):
    pass

class EnrollmentError(Exception):
    def __init__(self, err: str):
        self.err = err

class EnrolledUserError(Exception):
    pass

#handlers
def user_exist_handler(request: Request, exc: UserExistError):
    return JSONResponse(
        status_code=400,
        content='User already exist!'
)

def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content='User not Found!'
)

def invalid_password_handler(request: Request, exc: PasswordError):
    return JSONResponse(
        status_code=400,
        content='Incorrect password!'
)

def course_exist_handler(request: Request, exc: CourseExistError):
    return JSONResponse(
        status_code=400,
        content='Course already exist!'
)

def course_not_found_handler(request: Request, exc: CourseNotFoundError):
    return JSONResponse(
        status_code=404,
        content='Course not Found!'
)

def enrollment_not_found_handler(request: Request, exc: EnrollmentNotFoundError):
    return JSONResponse(
        status_code=404,
        content='Enrolment not Found!'
)

def enrollment_exist_handler(request: Request, exc: EnrollmentExistError):
    return JSONResponse(
        status_code=400,
        content='User already enrolled!'
)

def enrollment_error_handler(request: Request, exc: EnrollmentError):
    if exc.err == 'user':
        return JSONResponse(
            status_code=400,
            content='User is not active!'
        )
    elif exc.err == 'course':
        return JSONResponse(
            status_code=400,
            content='Course not open for enrollment!'
        )

def enrolled_user_handler(request: Request, exc: EnrolledUserError):
    return JSONResponse(
        status_code=404,
        content='No enrolled user at the moment!'
    )
