import time
from fastapi import FastAPI, Request
from app.routers import users, courses, enrollments
from app.services.errors import UserExistError, EnrollmentError
from app.services.errors import PasswordError, UserNotFoundError
from app.services.errors import CourseExistError, CourseNotFoundError
from app.services.errors import EnrollmentExistError, EnrollmentNotFoundError
from app.services.errors import EnrolledUserError
from app.services.errors import enrolled_user_handler
from app.services.errors import enrollment_not_found_handler, enrollment_exist_handler
from app.services.errors import user_exist_handler, invalid_password_handler
from app.services.errors import course_not_found_handler, enrollment_error_handler
from app.services.errors import user_not_found_handler, course_exist_handler
from app.core.utils import write_logs

app = FastAPI(title='EduTrack Lite API')

@app.middleware('http')
async def log_requests(request: Request, call_next):
    method, url = request.method, request.url
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    text = f'Method: {method}, URL: {url}, Time: {process_time}\n'
    write_logs(text)
    response.headers['X-App-Name'] = 'EduTrack'
    return response

#routers
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(courses.router, prefix='/courses', tags=['Courses'])
app.include_router(enrollments.router, prefix='/enrollments', tags=['Enrollments'])

#exception handlers
app.add_exception_handler(UserExistError, user_exist_handler)
app.add_exception_handler(PasswordError, invalid_password_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(CourseNotFoundError, course_not_found_handler)
app.add_exception_handler(CourseExistError, course_exist_handler)
app.add_exception_handler(EnrollmentNotFoundError, enrollment_not_found_handler)
app.add_exception_handler(EnrollmentExistError, enrollment_exist_handler)
app.add_exception_handler(EnrollmentError, enrollment_error_handler)
app.add_exception_handler(EnrolledUserError, enrolled_user_handler)
