import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_registration_valid_data():
    response = client.post('http://127.0.0.1:8000/api/customer/', data={
        'username': 'valid_username',
        'email': 'valid_email@gmail.com',
        'password': 'valid_password',
    }, format='json')

    assert response.status_code == 201
    assert response.data['message'] == 'User registered successfully. Please check your email for confirmation.'


@pytest.mark.django_db
def test_registration_invalid_data():
    response = client.post('http://127.0.0.1:8000/api/customer/', data={
        'username': 'valid_username',
        'email': 'invalid_email',
        'password': 'valid_password',
    }, format='json')

    assert response.status_code == 400
