from django.contrib.auth import login as last_login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from car_showroom.jwt_auth import get_tokens, refresh_access_token
from car.models import CarModel
from .serializers import LoginSerializer, RefreshTokenSerializer
from .models import Customer, CustomerPurchase


class AuthorizationService:
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

        last_login(request, user)

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


class CustomerStatisticsService:
    @staticmethod
    def total_cost_amount(customer):
        purchases = CustomerPurchase.objects.filter(customer=customer).aggregate(total_price=Sum('price'))
        return purchases['total_price'] or 0

    @staticmethod
    def count_of_purchases(customer):
        return CustomerPurchase.objects.filter(customer=customer).count()

    @staticmethod
    def list_of_bought_cars(customer):
        purchases = CustomerPurchase.objects.filter(customer=customer).values_list('model', flat=True)
        car_models = CarModel.objects.filter(id__in=purchases)
        return car_models
