from celery import shared_task
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from showroom.models import ShowroomCarCharacteristics
from .utils import get_filtered_cars, get_cheapest_provider_car, update_showroom_car, process_showroom_car
from .models import ShowroomCar


@shared_task
def get_showroom_cars(charact_id):
    charact = get_object_or_404(ShowroomCarCharacteristics, id=charact_id)
    showroom = charact.showroom
    cars = get_filtered_cars(charact)

    for car in cars:
        provider_car = get_cheapest_provider_car(car)
        if provider_car:
            update_showroom_car(showroom, car, provider_car)


@shared_task
def buy_car_from_provider():
    showroom_cars = ShowroomCar.objects.annotate(
        num_sales=Count('model__customerpurchase')
    ).order_by('-num_sales')

    for showroom_car in showroom_cars:
        process_showroom_car(showroom_car)


@shared_task
@transaction.atomic
def profitability_check():
    showroom_cars = ShowroomCar.objects.filter(is_active=True)
    for showroom_car in showroom_cars:
        cheapest_provider_car = get_cheapest_provider_car(showroom_car.model)
        if showroom_car.provider != cheapest_provider_car.provider:
            showroom_car.provider = cheapest_provider_car.provider
            showroom_car.save()
