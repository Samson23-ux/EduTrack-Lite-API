import pytest
from app.data.database import courses, enrollments
from app.schemas.courses import CourseCreate, CourseUpdate
from app.services.courses import course_service
from app.services.errors import EnrolledUserError
from app.services.errors import CourseExistError, CourseNotFoundError
from .conftest import fake_data1

def test_create_course(setup_course):
    assert 'id' in setup_course.model_dump()
    assert setup_course.title == fake_data1['title']

    with pytest.raises(CourseExistError) as exc:
        course_service.create_course(CourseCreate.model_validate(fake_data1))
    assert 'Course already exist!' == str(exc.value)

def test_get_courses(setup_course):
    courses = course_service.get_courses()
    assert len(courses) >= 1
    assert setup_course in courses

    with pytest.raises(CourseNotFoundError) as exc:
        course_service.get_courses(False)
    assert 'Course not found!' == str(exc.value)

def test_get_enrolled_users(setup_enrollment):
    enrolled_users = course_service.get_enrolled_users(setup_enrollment.course_id)
    assert len(enrolled_users) >= 1

    with pytest.raises(EnrolledUserError) as exc:
        enrollments.clear()
        course_service.get_enrolled_users('1')
    assert 'No enrolled user at the moment!' == str(exc.value)

def test_get_course(setup_course):
    course = course_service.get_course(setup_course.id)
    assert course.description == fake_data1['description']

    with pytest.raises(CourseNotFoundError) as exc:
        course_service.get_course('5')
    assert 'Course not found!' == str(exc.value)

def test_update_course(setup_course):
    course_update = CourseUpdate(
        title='llollo'
    )
    course = course_service.update_course(setup_course.id, course_update)
    assert course.title == course_update.title

def test_close_enrollment(setup_course):
    course_update = CourseUpdate(
        is_open=False
    )
    course = course_service.close_enrollment(setup_course.id, course_update)
    assert course.is_open is False

def test_delete_course(setup_course):
    course_service.delete_course(setup_course.id)
    assert setup_course not in courses
