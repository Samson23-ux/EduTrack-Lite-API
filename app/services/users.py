from app.core.utils import hash_password, quick_sort
from app.data.database import users
from app.schemas.users import User, UserCreate, UserUpdate, PasswordUpdate
from app.services.errors import  PasswordError
from app.services.errors import UserExistError, UserNotFoundError

class UserService:
    def is_user_exists(self, user: User) -> bool:
        exist = False
        for usr in users:
            name = user.name.lower().strip()
            if name == usr.name.lower().strip():
                exist = True
                break
        return exist

    def get_users(self, sort: str | None = None) -> list[User]:
        usrs = users.copy()
        if sort is not None:
            usrs = quick_sort(usrs)
        if not usrs:
            raise UserNotFoundError('User not found!')
        return usrs

    def get_user(self, user_id: str) -> User:
        for user in users:
            if user.id == user_id:
                return user
        raise UserNotFoundError('User not found!')

    def create_user(self, user_create: UserCreate) -> User:
        user = User(
            id=str(len(users) + 1),
            **user_create.model_dump()
        )
        user.password = hash_password(user.password)

        if self.is_user_exists(user):
            raise UserExistError('User already exist!')

        users.append(user)
        return self.get_user(user.id)

    def update_user(
            self,
            user_id: str,
            user_update: UserUpdate
    ) -> User:
        user = self.get_user(user_id)

        if hash_password(user_update.current_password) != user.password:
            raise PasswordError('Incorrect password!')

        user_update = user_update.model_dump(exclude_unset=True, exclude={'current_password'})
        for k, v in user_update.items():
            setattr(user, k, v)

        return self.get_user(user_id)

    def deactivate_user(
            self,
            user_id: str,
            user_update: UserUpdate
    ) -> User:
        user = self.get_user(user_id)

        if hash_password(user_update.current_password) != user.password:
            raise PasswordError('Incorrect password!')

        user.is_active = user_update.is_active

        return self.get_user(user_id)

    def update_password(
            self,
            user_id: str,
            password_update: PasswordUpdate
    ) -> User:
        user = self.get_user(user_id)

        if hash_password(password_update.current_password) != user.password:
            raise PasswordError('Incorrect password!')

        user.password = hash_password(password_update.new_password)

        return self.get_user(user_id)

    def delete_user(self, user_id: str, current_password: str):
        user = self.get_user(user_id)

        if hash_password(current_password) != user.password:
            raise PasswordError('Incorrect password!')

        users.remove(user)

user_service = UserService()
