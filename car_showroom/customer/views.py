from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from car_showroom.jwt_auth import get_tokens, refresh_access_token
from .serializers import CustomerSerializer, LoginSerializer, RefreshTokenSerializer
from .models import Customer


class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=400)

        user_id = user.id
        payload = {"user_id": user_id, "username": username}

        tokens = get_tokens(payload)

        return Response(tokens)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']

        access_token = refresh_access_token(refresh_token)

        return Response(access_token)
