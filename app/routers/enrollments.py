from fastapi import APIRouter, Query
from app.schemas.enrollments import EnrollmentCreate, Response
from app.services.enrollments import enrol_service

router = APIRouter()

@router.get('/', response_model=Response)
def get_enrollments(
    completed: bool = Query(None, description='Filter by completed course(True/False)')
):
    enrollments = enrol_service.get_enrollments(completed)

    return Response(message='Enrollments retrieved successfully!',
                    data=enrollments)

@router.get('/users/{user_id}/', response_model=Response)
def get_user_enrollments(user_id: str):
    enrollments = enrol_service.get_user_enrollments(user_id)

    return Response(message='User Enrollments retrieved successfully!',
                    data=enrollments)

@router.get('/{enrollment_id}/', response_model=Response)
def get_enrollment(enrollment_id: str):
    enrollment = enrol_service.get_enrollment(enrollment_id)

    return Response(message='Enrollment retrieved successfully!', data=enrollment)

@router.post('/', status_code=201, response_model=Response)
def enrol_for_course(enrollment_create: EnrollmentCreate):
    enrollment = enrol_service.enrol(enrollment_create)

    return Response(message='Course enrolled successfully!', data=enrollment)

@router.patch('/{enrollment_id}/', response_model=Response)
def mark_course_complete(enrollment_id: str):
    enrollment = enrol_service.mark_course_complete(enrollment_id)

    return Response(message='Course mark completed successfully!', data=enrollment)
