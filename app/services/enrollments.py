from app.data.database import enrollments
from app.services.users import user_service
from app.services.courses import course_service
from app.schemas.enrollments import Enrollment, EnrollmentCreate
from app.services.errors import EnrollmentError
from app.services.errors import EnrollmentExistError, EnrollmentNotFoundError

class EnrollmentService:
    def has_user_enrolled(self, user_id: str, course_id: str) -> bool:
        for enr in enrollments:
            if enr.user_id == user_id and enr.course_id == course_id:
                return True
        return False

    def get_enrollments(self, completed: str | None = None) -> list[Enrollment]:
        enrols = enrollments.copy()
        if completed is not None:
            enrols = [enr for enr in enrollments if enr.completed is completed]

        if not enrols:
            raise EnrollmentNotFoundError('Enrolment not Found!')

        return enrols

    def get_user_enrollments(self, user_id: str) -> list[Enrollment]:
        user_enrollments = []
        for enrollment in enrollments:
            if enrollment.user_id == user_id:
                user_enrollments.append(enrollment)

        if not user_enrollments:
            raise EnrollmentNotFoundError('Enrolment not Found!')

        return user_enrollments

    def get_enrollment(self, enrollment_id: str) -> Enrollment:
        for enrollment in enrollments:
            if enrollment.id == enrollment_id:
                return enrollment
        raise EnrollmentNotFoundError('Enrolment not Found!')

    def enrol(self, enrollment_create: EnrollmentCreate) -> Enrollment:
        enrollment = Enrollment(
            id=str(len(enrollments) + 1),
            **enrollment_create.model_dump()
        )

        if self.has_user_enrolled(enrollment.user_id, enrollment.course_id):
            raise EnrollmentExistError('User already enrolled!')

        user = user_service.get_user(enrollment.user_id)
        if not user.is_active:
            raise EnrollmentError('user')

        course = course_service.get_course(enrollment.course_id)
        if not course.is_open:
            raise EnrollmentError('course')

        enrollments.append(enrollment)
        return self.get_enrollment(enrollment.id)

    def mark_course_complete(self, enrollment_id: str):
        enrollment = self.get_enrollment(enrollment_id)

        enrollment.completed = True

        return self.get_enrollment(enrollment_id)

enrol_service = EnrollmentService()
