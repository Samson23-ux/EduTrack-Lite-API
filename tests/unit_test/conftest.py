import pytest
from datetime import date
from app.services.users import user_service
from app.services.courses import course_service
from app.services.enrollments import enrol_service
from app.schemas.users import UserCreate
from app.schemas.courses import CourseCreate
from app.schemas.enrollments import EnrollmentCreate
from app.data.database import users, courses, enrollments

fake_data = {
    'name': 'aaaaaaaa',
    'email': 'a@gmail.com',
    'password': 'aaaaaaaa',
    'is_active': True
}

fake_data1 = {
    'title': 'bbbbbbbb',
    'description': 'bababa',
    'is_open': True
}

fake_data2 = {
    'user_id': '1',
    'course_id': '1',
    'enrolled_date': "2025-10-03",
    'completed': False
}

fake_data3 = {
    'name': 'cccccccc',
    'email': 'c@gmail.com',
    'password': 'cccccccc',
    'is_active': True
}

@pytest.fixture(autouse=True)
def reset_db():
    users.clear()
    courses.clear()
    enrollments.clear()

# create user
@pytest.fixture
def setup_user():
    user_create = UserCreate.model_validate(fake_data)
    user_create2 = UserCreate.model_validate(fake_data3)
    user = user_service.create_user(user_create)
    user_service.create_user(user_create2)
    return user

@pytest.fixture
def setup_course():
    course_create = CourseCreate.model_validate(fake_data1)
    course = course_service.create_course(course_create)
    return course

@pytest.fixture
def setup_enrollment(setup_user, setup_course):
    enrollment_create = EnrollmentCreate.model_validate(fake_data2)
    enrollment = enrol_service.enrol(enrollment_create)
    return enrollment
