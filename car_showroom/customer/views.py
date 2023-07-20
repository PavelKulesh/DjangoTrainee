from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from car_showroom.jwt_auth import get_tokens, refresh_access_token
from .serializers import CustomerSerializer, LoginSerializer, RefreshTokenSerializer
from .models import Customer


class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        action = request.data.get('action')

        if action == 'login':
            return self.login(request)
        elif action == 'refresh':
            return self.refresh_token(request)
        else:
            return Response({'error': 'Invalid action! Choose login or refresh.'}, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = Customer.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = user.id
        payload = {"user_id": user_id, "username": username}

        tokens = get_tokens(payload)

        return Response(tokens, status=status.HTTP_200_OK)

    def refresh_token(self, request):
        serializer = RefreshTokenSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data['refresh']

        access_token = refresh_access_token(refresh_token)

        return Response(access_token, status=status.HTTP_200_OK)
