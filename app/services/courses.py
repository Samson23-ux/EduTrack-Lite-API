from app.data.database import courses, enrollments
from app.services.users import user_service
from app.schemas.courses import Course, CourseCreate, CourseUpdate
from app.services.errors import CourseExistError, CourseNotFoundError, EnrolledUserError

class CourseService:
    def is_course_exists(self, course: Course) -> bool:
        exists = False
        for cs in courses:
            title = course.title.lower().strip()
            if title == cs.title.lower().strip():
                exists = True
                break
        return exists

    def get_courses(self, is_open: str | None = None) -> list[Course]:
        cors = courses.copy()
        if is_open is not None:
            cors = [cs for cs in courses if cs.is_open is is_open]

        if not cors:
            raise CourseNotFoundError('Course not found!')
        return cors

    def get_user_courses(self, user_id: str):
        user_courses = []
        for enrollment in enrollments:
            if enrollment.user_id == user_id:
                user_courses.append(self.get_course(enrollment.course_id))

        if not user_courses:
            raise CourseNotFoundError('Course not found!')
        return user_courses

    def get_enrolled_users(self, course_id: str):
        enrolled_users = []

        for enrollment in enrollments:
            if enrollment.course_id == course_id:
                user = user_service.get_user(enrollment.user_id)
                enrolled_users.append(user)

        if not enrolled_users:
            raise EnrolledUserError('No enrolled user at the moment!')

        return enrolled_users

    def get_course(self, course_id: str) -> Course:
        for course in courses:
            if course.id == course_id:
                return course
        raise CourseNotFoundError('Course not found!')

    def create_course(self, course_create: CourseCreate) -> Course:
        course = Course(
            id=str(len(courses) + 1),
            **course_create.model_dump()
        )

        if self.is_course_exists(course):
            raise CourseExistError('Course already exist!')

        courses.append(course)
        return self.get_course(course.id)

    def update_course(
        self,
        course_id: str,
        course_update: CourseUpdate
    ) -> Course:
        course = self.get_course(course_id)

        course_update = course_update.model_dump(exclude_unset=True)

        for k, v in course_update.items():
            setattr(course, k, v)

        return self.get_course(course_id)

    def close_enrollment(
        self,
        course_id: str,
        course_update: CourseUpdate
    ) -> Course:
        course = self.get_course(course_id)

        course.is_open = course_update.is_open

        return self.get_course(course_id)

    def delete_course(self, course_id: str):
        course = self.get_course(course_id)

        courses.remove(course)

course_service = CourseService()
