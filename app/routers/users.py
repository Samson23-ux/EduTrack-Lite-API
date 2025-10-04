from fastapi import APIRouter, Query, Form
from app.services.users import user_service
from app.schemas.users import UserCreate, UserUpdate, PasswordUpdate, Response

router = APIRouter()

@router.get('/', response_model=Response)
def get_users(
    sort: str = Query(None, description='Sort users by username eg sort=username')
):
    users = user_service.get_users(sort)

    return Response(message='Users retrieved successfully!', data=users)

@router.get('/{user_id}/', response_model=Response)
def get_user(user_id: str):
    user = user_service.get_user(user_id)

    return Response(message='User retrieved successfully!', data=user)

@router.post('/', status_code=201, response_model=Response)
def create_user(user_create: UserCreate):
    user = user_service.create_user(user_create)

    return Response(message='User created successfully!', data=user)

@router.patch('/{user_id}/', response_model=Response)
def update_user(user_id: str, user_update: UserUpdate):
    user = user_service.update_user(user_id, user_update)

    return Response(message='User updated successfully!', data=user)

@router.patch('/{user_id}/deactivate/', response_model=Response)
def deactivate_user(user_id: str, user_update: UserUpdate):
    user = user_service.deactivate_user(user_id, user_update)

    return Response(message='User deactivated successfully!', data=user)

@router.patch('/{user_id}/password/', response_model=Response)
def update_password(user_id: str, password_update: PasswordUpdate):
    user = user_service.update_password(user_id, password_update)

    return Response(message='Password updated successfully!', data=user)

@router.delete('/{user_id}/', status_code=204)
def delete_user(user_id: str, current_password: str = Form(...)):
    user_service.delete_user(user_id, current_password)

    return Response(message='User deleted successfully!')
