import pytest
from rest_framework.test import APIClient

from car_showroom.jwt_auth import get_tokens

client = APIClient()


@pytest.mark.django_db
def test_login_valid_credentials(user):
    response = client.post('http://127.0.0.1:8000/api/customer/login/', data={
        'username': 'valid_username',
        'password': 'valid_password',
        'action': 'login',
    }, format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_invalid_credentials(user):
    response = client.post('http://127.0.0.1:8000/api/customer/login/', data={
        'username': 'invalid_username',
        'password': 'invalid_password',
        'action': 'login',
    }, format='json')

    assert response.status_code == 400
    assert response.data['error'] == 'Invalid credentials'


@pytest.mark.django_db
def test_login_invalid_action(user):
    response = client.post('http://127.0.0.1:8000/api/customer/login/', data={
        'username': 'valid_username',
        'password': 'valid_password',
        'action': '',
    }, format='json')

    assert response.status_code == 400
    assert response.data['error'] == 'Invalid action! Choose login or refresh.'


@pytest.mark.django_db
def test_access_with_valid_token(user):
    payload = {'user_id': user.id}
    tokens = get_tokens(payload)
    response = client.get(
        'http://127.0.0.1:8000/api/customer/',
        headers={
            'Authorization': f'JWT {tokens["access"]}',
        },
        format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_access_with_invalid_token():
    with pytest.raises(Exception):
        response = client.get(
            'http://127.0.0.1:8000/api/customer/',
            headers={
                'Authorization': 'JWT invalid_access_token',
            },
            format='json')
