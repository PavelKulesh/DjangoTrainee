from celery import shared_task
from django.shortcuts import get_object_or_404
from showroom.models import ShowroomCarCharacteristics
from .services import get_filtered_cars, get_cheapest_provider_car, update_showroom_car, number_of_sales, \
    process_showroom_car
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
    showroom_cars = ShowroomCar.objects.select_related('showroom', 'model', 'provider').filter(is_active=True)
    showroom_cars = sorted(showroom_cars, key=lambda car: number_of_sales(car.showroom, car.model), reverse=True)

    for showroom_car in showroom_cars:
        process_showroom_car(showroom_car)


@shared_task
def profitability_check():
    showroom_cars = ShowroomCar.objects.filter(is_active=True)
    for showroom_car in showroom_cars:
        cheapest_provider_car = get_cheapest_provider_car(showroom_car.model)
        if showroom_car.provider != cheapest_provider_car.provider:
            showroom_car.provider = cheapest_provider_car.provider
            showroom_car.save()
