import pytest
from app.services.users import user_service
from app.services.courses import course_service
from app.services.enrollments import enrol_service
from app.data.database import enrollments
from app.schemas.enrollments import EnrollmentCreate
from app.services.errors import EnrollmentError
from app.services.errors import EnrollmentExistError, EnrollmentNotFoundError
from .conftest import fake_data2

def test_get_enrollment(setup_enrollment):
    enrollment = enrol_service.get_enrollment(setup_enrollment.id)
    assert enrollment.course_id == setup_enrollment.course_id

    with pytest.raises(EnrollmentNotFoundError) as exc:
        enrol_service.get_enrollment('7')
    assert 'Enrolment not Found!' == str(exc.value)

def test_enrol(setup_enrollment):
    assert 'id' in setup_enrollment.model_dump()
    assert fake_data2['user_id'] == setup_enrollment.user_id

    with pytest.raises(EnrollmentExistError) as exc:
        enrol_service.enrol(EnrollmentCreate.model_validate(fake_data2))
    assert 'User already enrolled!' == str(exc.value)

    enrollments.clear()
    with pytest.raises(EnrollmentError) as exc:
        user = user_service.get_user(setup_enrollment.user_id)
        user.is_active = False
        enrol_service.enrol(EnrollmentCreate.model_validate(fake_data2))

    with pytest.raises(EnrollmentError) as exc:
        user.is_active = True
        course = course_service.get_course(setup_enrollment.course_id)
        course.is_open = False
        enrol_service.enrol(EnrollmentCreate.model_validate(fake_data2))

def test_mark_course_complete(setup_enrollment):
    enrollment = enrol_service.mark_course_complete(setup_enrollment.id)
    assert enrollment.completed is True

def test_get_enrollments(setup_enrollment):
    user_enrollments = enrol_service.get_enrollments()
    assert setup_enrollment in user_enrollments
    assert len(user_enrollments) >= 1

    with pytest.raises(EnrollmentNotFoundError) as exc:
        enrol_service.get_enrollments(True)
    assert 'Enrolment not Found!' == str(exc.value)

def test_get_user_enrollments(setup_enrollment):
    user_enrollments = enrol_service.get_user_enrollments(setup_enrollment.user_id)
    assert setup_enrollment in user_enrollments

    with pytest.raises(EnrollmentNotFoundError) as exc:
        enrol_service.get_user_enrollments('6')
    assert 'Enrolment not Found!' == str(exc.value)
