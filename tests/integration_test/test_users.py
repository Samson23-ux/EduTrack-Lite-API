from app.core.utils import hash_password
from .conftest import fake_data, fake_data2

def test_get_users(test_client, setup_user):
    response = test_client.get(
        '/users/',
        params={'sort': 'name'}
    )

    assert response.status_code == 200
    assert response.json()['data'][0]['id'] == '2'

def test_get_user(test_client, setup_user):
    response = test_client.get(
        '/users/1/'
    )

    assert response.status_code == 200
    assert response.json()['data']['name'] == fake_data2['name']

def test_no_user(test_client, setup_user):
    response = test_client.get(
        '/users/4/'
    )
    assert response.status_code == 404

def test_create_user(test_client, setup_user):
    assert setup_user.status_code == 201
    assert 'id' in setup_user.json()['data']

def test_duplicate_user(test_client, setup_user):
    response = test_client.post(
        '/users/',
        json=fake_data
    )

    assert response.status_code == 400

def test_update_user(test_client, setup_user):
    response = test_client.patch(
        '/users/2/',
        json={
            'name': 'aabbabba',
            'current_password': fake_data['password']
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['name'] == 'aabbabba'

def test_deactivate_user(test_client, setup_user):
    response = test_client.patch(
        '/users/1/deactivate/',
        json={
            'is_active': False,
            'current_password': fake_data2['password']
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['is_active'] is False

def test_update_password(test_client, setup_user):
    response = test_client.patch(
        '/users/1/password/',
        json={
            'current_password': fake_data2['password'],
            'new_password': 'False'
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['password'] == hash_password('False')

def test_delete_user(test_client, setup_user):
    response = test_client.request(
        'DELETE',
        '/users/1/',
        data={'current_password': fake_data2['password']}
    )

    assert response.status_code == 204
