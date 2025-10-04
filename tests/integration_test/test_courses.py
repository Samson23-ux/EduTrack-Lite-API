from .conftest import fake_data3, fake_data4

def test_create_course(setup_course):
    assert setup_course.status_code == 201
    assert 'id' in setup_course.json()['data']

def test_duplicate_course(test_client, setup_course):
    response = test_client.post(
        '/courses/',
        json=fake_data4
    )

    assert response.status_code == 400

def test_get_courses(test_client, setup_course):
    response = test_client.get(
        '/courses/'
    )

    assert response.status_code == 200
    assert len(response.json()['data']) >= 1

def test_get_course(test_client, setup_course):
    response = test_client.get(
        '/courses/1/'
    )

    assert response.status_code == 200
    assert response.json()['data']['title'] == fake_data3['title']

def test_course_not_found(test_client, setup_course):
    response = test_client.get(
        '/courses/4/'
    )

    assert response.status_code == 404

def test_get_enrolled_users(test_client, setup_enrollments):
    response = test_client.get(
        '/courses/1/users/'
    )

    assert response.status_code == 200
    assert len(response.json()['data']) >= 1

def test_no_enrolled_users(test_client, setup_course):
    response = test_client.get(
        '/courses/2/users/'
    )

    assert response.status_code == 404

def test_update_course(test_client, setup_course):
    response = test_client.patch(
        '/courses/1/',
        json={'description': 'rrtrrtr'}
    )

    assert response.status_code == 200
    assert response.json()['data']['description'] == 'rrtrrtr'

def test_close_enrollment(test_client, setup_course):
    response = test_client.patch(
        '/courses/2/close-enrollment/',
        json={'is_open': False}
    )

    assert response.status_code == 200
    assert response.json()['data']['is_open'] is False

def test_delete_course(test_client, setup_course):
    test_client.delete(
        '/courses/2/'
    )

    response = test_client.get(
        '/courses/2/'
    )

    assert response.status_code == 404
