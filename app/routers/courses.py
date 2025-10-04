from fastapi import APIRouter, Query
from app.services.courses import course_service
from app.schemas.courses import CourseCreate, CourseUpdate, Response

router = APIRouter()

@router.get('/', response_model=Response)
def get_courses(is_open: bool = Query(None, description='Filter by open course (True/False)')):
    courses = course_service.get_courses(is_open)

    return Response(message='Courses retrieved successfully!', data=courses)

@router.get('/{course_id}/users/', response_model=Response)
def get_enrolled_users(course_id: str):
    enrolled_users = course_service.get_enrolled_users(course_id)

    return Response(message='Enrolled users retrieved successfully!',
                    data=enrolled_users)

@router.get('/{course_id}/', response_model=Response)
def get_course(course_id: str):
    course = course_service.get_course(course_id)

    return Response(message='Course retrieved successfully!', data=course)

@router.post('/', status_code=201, response_model=Response)
def create_course(course_create: CourseCreate):
    course = course_service.create_course(course_create)

    return Response(message='Course created successfully!', data=course)

@router.patch('/{course_id}/', response_model=Response)
def update_course(course_id: str, course_update: CourseUpdate):
    course = course_service.update_course(course_id, course_update)

    return Response(message='Course updated successfully!', data=course)

@router.patch('/{course_id}/close-enrollment/', response_model=Response)
def close_enrollment(course_id: str, course_update: CourseUpdate):
    course = course_service.close_enrollment(course_id, course_update)

    return Response(message='Course enrollment closed successfully!', data=course)

@router.delete('/{course_id}/', status_code=204)
def delete_course(course_id: str):
    course_service.delete_course(course_id)

    return Response(message='Course deleted successfully!')
