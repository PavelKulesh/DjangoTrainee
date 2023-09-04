from car_showroom.jwt_auth import generate_token, check_token, refresh_access_token, get_tokens

ACCESS_TOKEN_EXPIRATION = 3600


def test_generate_token():
    payload = {'user_id': 123}
    token = generate_token(payload, ACCESS_TOKEN_EXPIRATION)
    assert token is not None


def test_get_tokens():
    payload = {'user_id': 123}
    tokens = get_tokens(payload)
    assert 'access' in tokens
    assert 'refresh' in tokens
    assert tokens['access'] is not None
    assert tokens['refresh'] is not None


def test_refresh_access_token():
    payload = {'user_id': 123}
    tokens = get_tokens(payload)
    result = refresh_access_token(tokens['refresh'])
    assert result is not None
    assert 'access' in result


def test_check_valid_token():
    payload = {'user_id': 123}
    token = generate_token(payload, ACCESS_TOKEN_EXPIRATION)
    result = check_token(token)
    assert result is not None
    assert result['user_id'] == payload['user_id']


def test_check_expired_token():
    payload = {'user_id': 123}
    expired_token = generate_token(payload, -1)
    result = check_token(expired_token)
    assert result is None
