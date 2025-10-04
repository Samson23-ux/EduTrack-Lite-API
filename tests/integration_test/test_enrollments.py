from .conftest import fake_data5, fake_data6

def test_get_enrollments(test_client, setup_enrollments):
    response = test_client.get(
        '/enrollments/'
    )

    assert response.status_code == 200
    assert len(response.json()['data']) >= 1

def test_get_user_enrollments(test_client, setup_enrollments):
    response = test_client.get(
        '/enrollments/users/1/'
    )

    assert response.status_code == 200
    assert len(response.json()['data']) >= 1

def test_get_enrollment(test_client, setup_enrollments):
    response = test_client.get(
        '/enrollments/1/'
    )

    assert response.status_code == 200
    assert len(response.json()['data']) >= 1

def test_enrollment_not_found(test_client, setup_enrollments):
    response = test_client.get(
        '/enrollments/3/'
    )

    assert response.status_code == 404

def test_enrol_for_course(setup_enrollments):
    assert setup_enrollments.status_code == 201
    assert 'id' in setup_enrollments.json()['data']

def test_duplicate_enrollment(test_client, setup_enrollments):
    response = test_client.post(
        '/enrollments/',
        json=fake_data6
    )

    assert response.status_code == 400

def test_mark_course_complete(test_client, setup_enrollments):
    response = test_client.patch(
        '/enrollments/1/'
    )

    assert response.status_code == 200
    assert response.json()['data']['completed'] is True
