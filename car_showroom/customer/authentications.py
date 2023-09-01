from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from car_showroom.jwt_auth import check_token
from .models import Customer


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            _, token = auth_header.split()
            payload = check_token(token)
            user_id = payload.get('user_id')
        except Exception as e:
            raise Exception("Invalid Access Token")

        try:
            user = Customer.objects.get(id=user_id)
        except Customer.DoesNotExist:
            raise AuthenticationFailed('No user found with this token')

        return (user, token)
