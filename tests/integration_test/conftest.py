import pytest
from datetime import date
from app.main import app
from fastapi.testclient import TestClient
from app.data.database import users, courses, enrollments

fake_data = {
    'name': 'aaaaaaaa',
    'email': 'a@gmail.com',
    'password': 'aaaaaaaa',
    'is_active': True
}

fake_data2 = {
    'name': 'cccccccc',
    'email': 'c@gmail.com',
    'password': 'cccccccc',
    'is_active': True
}

fake_data3 = {
    'title': 'bbbbbbbb',
    'description': 'bababa',
    'is_open': True
}

fake_data4 = {
    'title': 'tttttttt',
    'description': 'tatatat',
    'is_open': True
}

fake_data5 = {
    'user_id': '1',
    'course_id': '1',
    'enrolled_date': "2025-10-03",
    'completed': False
}

fake_data6 = {
    'user_id': '2',
    'course_id': '1',
    'enrolled_date': "2025-10-03",
    'completed': False
}

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
def reset_db():
    users.clear()
    courses.clear()
    enrollments.clear()

@pytest.fixture
def setup_user(test_client):
    test_client.post(
        '/users/',
        json=fake_data2
    )

    response = test_client.post(
        '/users/',
        json=fake_data
    )
    return response

@pytest.fixture
def setup_course(test_client):
    response = test_client.post(
        '/courses/',
        json=fake_data3
    )

    test_client.post(
        '/courses/',
        json=fake_data4
    )
    return response

@pytest.fixture
def setup_enrollments(setup_user, setup_course, test_client):
    response = test_client.post(
        '/enrollments/',
        json=fake_data5
    )

    test_client.post(
        '/enrollments/',
        json=fake_data6
    )
    return response
