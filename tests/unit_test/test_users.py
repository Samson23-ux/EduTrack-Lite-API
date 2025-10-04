import pytest
from app.core.utils import hash_password
from app.services.users import user_service
from app.services.errors import  PasswordError
from app.services.errors import UserExistError, UserNotFoundError
from app.schemas.users import UserCreate, UserUpdate, PasswordUpdate
from .conftest import fake_data

def test_create_user(setup_user):
    assert 'id' in setup_user.model_dump()
    assert setup_user.name == fake_data['name']

    with pytest.raises(UserExistError) as exc:
        user_create = UserCreate.model_validate(fake_data)
        user_service.create_user(user_create)
    assert 'User already exist!' == str(exc.value)

def test_get_users(setup_user):
    users = user_service.get_users('name')
    assert len(users) >= 1

def test_get_user(setup_user):
    user = user_service.get_user(setup_user.id)
    assert user.email == fake_data['email']

    with pytest.raises(UserNotFoundError) as exc:
        user_service.get_user('6')
    assert 'User not found!' == str(exc.value)

def test_update_user(setup_user):
    user_update = UserUpdate(
        email='k@gmail.com',
        current_password=fake_data['password']
    )
    user = user_service.update_user(setup_user.id, user_update)
    assert user.email == user_update.email

    with pytest.raises(PasswordError) as exc:
        user_update.current_password = 'passsssworddd'
        user_service.update_user(setup_user.id, user_update)
    assert 'Incorrect password!' == str(exc.value)

def test_deactivate_user(setup_user):
    user_update = UserUpdate(
        is_active=False,
        current_password=fake_data['password']
    )
    user = user_service.deactivate_user(setup_user.id, user_update)
    assert user.is_active is False

    with pytest.raises(PasswordError) as exc:
        user_update.current_password = 'passsssworddd'
        user_service.deactivate_user(setup_user.id, user_update)
    assert 'Incorrect password!' == str(exc.value)

def test_update_password(setup_user):
    password_update = PasswordUpdate(
        current_password=fake_data['password'],
        new_password='uuuduuuduuduudu'
    )
    user = user_service.update_password(setup_user.id, password_update)

    assert hash_password(password_update.new_password) == user.password

    with pytest.raises(PasswordError) as exc:
        password_update.current_password = 'passsssworddd'
        user_service.update_password(setup_user.id, password_update)
    assert 'Incorrect password!' == str(exc.value)

def test_delete_user(setup_user):
    user_service.delete_user(setup_user.id, fake_data['password'])
    users = user_service.get_users()

    assert users[0].id != setup_user.id
