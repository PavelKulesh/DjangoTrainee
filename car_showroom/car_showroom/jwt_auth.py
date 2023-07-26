import base64
import hashlib
import hmac
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRATION = int(os.getenv('ACCESS_TOKEN_EXPIRATION'))
REFRESH_TOKEN_EXPIRATION = int(os.getenv('REFRESH_TOKEN_EXPIRATION'))


def generate_token(payload, expiration):
    current_time = time.time()
    payload['exp'] = current_time + expiration

    header = {
        'alg': 'HS256',
        'type': 'JWT',
    }

    header_base64 = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).rstrip(b'=')
    payload_base64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).rstrip(b'=')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), f'{header_base64}.{payload_base64}'.encode('utf-8'),
                         hashlib.sha256)
    signature_base64 = base64.urlsafe_b64encode(signature.digest()).rstrip(b'=')

    token = f"{header_base64.decode('utf-8')}.{payload_base64.decode('utf-8')}.{signature_base64.decode('utf-8')}"

    return token


def get_tokens(payload):
    access_token = generate_token(payload, ACCESS_TOKEN_EXPIRATION)
    refresh_token = generate_token(payload, REFRESH_TOKEN_EXPIRATION)

    tokens = {
        'access': access_token,
        'refresh': refresh_token,
    }

    return tokens


def refresh_access_token(refresh_token):
    if check_token(refresh_token):
        _, payload_base64, _ = (part.encode('utf-8') for part in refresh_token.split('.'))
        payload = json.loads(base64.urlsafe_b64decode(payload_base64 + b'=='))

        new_access_token = generate_token(payload, ACCESS_TOKEN_EXPIRATION)

        return {'access': new_access_token}

    return {'error': 'Invalid Refresh Token'}


def check_token(token):
    header_base64, payload_base64, signature_base64 = (part.encode('utf-8') for part in token.split('.'))

    expected_signature = hmac.new(SECRET_KEY.encode('utf-8'), f'{header_base64}.{payload_base64}'.encode('utf-8'),
                                  hashlib.sha256)
    expected_signature_base64 = base64.urlsafe_b64encode(expected_signature.digest()).rstrip(b'=')

    if not hmac.compare_digest(expected_signature_base64, signature_base64):
        return None

    payload = json.loads(base64.urlsafe_b64decode(payload_base64 + b'=='))

    if payload.get('exp', 0) < time.time():
        return None

    return payload
