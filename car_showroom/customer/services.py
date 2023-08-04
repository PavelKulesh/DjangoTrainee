from _decimal import Decimal
from django.contrib.auth import login as last_login
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Case, When, Max, DecimalField, F
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from car_showroom.jwt_auth import get_tokens, refresh_access_token
from showroom.models import ShowroomCar
from .serializers import LoginSerializer, RefreshTokenSerializer
from .models import Customer, CustomerPurchase


def get_data_for_serializer(obj, request):
    if not request.user.is_superuser:
        return {key: value for key, value in request.data.items() if key in obj.allowed_fields}
    else:
        return request.data


def login(request):
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


def refresh_token(request):
    serializer = RefreshTokenSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    refresh_token = serializer.validated_data['refresh']

    access_token = refresh_access_token(refresh_token)

    return Response(access_token, status=status.HTTP_200_OK)


def get_cheapest_showroom_car(car):
    showroom_cars = ShowroomCar.objects.filter(model=car, quantity__gte=1, is_active=True).annotate(
        max_discount=Case(
            When(showroom__showroomdiscount__is_active=True,
                 showroom__showroomdiscount__start_at__lte=timezone.now(),
                 showroom__showroomdiscount__end_at__gte=timezone.now(),
                 then=Max('showroom__showroomdiscount__percent')),
            default=0,
            output_field=DecimalField()
        )
    ).annotate(
        final_price=(F('showroom_price') - F('showroom_price') * F('max_discount') / 100)
    )

    return showroom_cars.order_by('final_price').first()


def get_individual_discount(customer, showroom):
    number_of_purchases = CustomerPurchase.objects.filter(customer=customer, showroom=showroom).count()
    return showroom.discount_percent if number_of_purchases and (
            number_of_purchases >= showroom.quantity_for_discount) else 0


def get_price_with_discount(individual_discount, showroom_car):
    return showroom_car.showroom_price * Decimal(1 - (showroom_car.max_discount + individual_discount) / 100)


def process_offered_car(offer, showroom_car, customer, model):
    showroom = showroom_car.showroom
    individual_discount = get_individual_discount(customer, showroom)
    final_price = get_price_with_discount(individual_discount, showroom_car)

    if offer.max_price >= final_price:
        process_successful_purchase(offer, showroom, customer, showroom_car, final_price, model)


@transaction.atomic
def process_successful_purchase(offer, showroom, customer, showroom_car, final_price, model):
    showroom.balance += final_price
    customer.balance -= final_price
    showroom_car.quantity -= 1

    customer_purchase, created = CustomerPurchase.objects.get_or_create(
        customer=customer,
        showroom=showroom,
        model=model,
        price=final_price,
    )

    offer.delete()

    showroom.save()
    customer.save()
    showroom_car.save()
