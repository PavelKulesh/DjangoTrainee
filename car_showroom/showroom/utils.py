import os
from _decimal import Decimal
from django.db import transaction
from django.db.models import F, Max, Sum, Case, When, DecimalField
from django.utils import timezone
from provider.models import ProviderCar
from showroom.models import ShowroomCar, ShowroomPurchase
from car.models import CarModel


def get_filtered_cars(charact):
    return CarModel.objects.filter(
        brand=charact.brand,
        fuel_type=charact.fuel,
        transmission=charact.transmission,
        is_active=True,
    )


def get_cheapest_provider_car(car, provider=None):
    provider_cars = ProviderCar.objects.filter(model=car, is_active=True)

    if provider:
        provider_cars = provider_cars.filter(provider=provider)

    provider_cars = provider_cars.annotate(
        max_discount=Case(
            When(provider__providerdiscount__is_active=True,
                 provider__providerdiscount__start_at__lte=timezone.now(),
                 provider__providerdiscount__end_at__gte=timezone.now(),
                 then=Max('provider__providerdiscount__percent')),
            default=0,
            output_field=DecimalField()
        )
    ).annotate(
        final_price=(F('provider_price') - F('provider_price') * F('max_discount') / 100)
    )

    return provider_cars.order_by('final_price').first()


def update_showroom_car(showroom, car, provider_car):
    showroom_car, created = ShowroomCar.objects.get_or_create(
        showroom=showroom,
        model=car,
        provider=provider_car.provider,
    )
    showroom_car.showroom_price = provider_car.final_price * Decimal(os.getenv('SHOWROOM_PERCENT'))
    showroom_car.save()


def get_individual_discount(showroom, provider):
    number_of_purchases = ShowroomPurchase.objects.filter(showroom=showroom, provider=provider).aggregate(
        number_of_purchases=Sum('quantity'))['number_of_purchases']
    return provider.discount_percent if number_of_purchases and (
            number_of_purchases >= provider.quantity_for_discount) else 0


def process_showroom_car(showroom_car):
    showroom = showroom_car.showroom
    provider = showroom_car.provider
    model = showroom_car.model

    provider_car = ProviderCar.objects.filter(provider=provider, model=model, is_active=True).first()
    if provider_car:
        individual_discount = get_individual_discount(showroom, provider)
        price_with_discount = get_price_with_discount(provider_car.provider_price, individual_discount, model, provider)
        if showroom.balance >= price_with_discount:
            process_successful_purchase(showroom, provider, model, showroom_car, price_with_discount)


def get_price_with_discount(provider_price, individual_discount, model, provider):
    max_discount = get_cheapest_provider_car(car=model, provider=provider).max_discount
    return provider_price * Decimal(1 - (max_discount + individual_discount) / 100)


@transaction.atomic
def process_successful_purchase(showroom, provider, model, showroom_car, price_with_discount):
    quantity = showroom.balance // max(price_with_discount, 1)
    showroom.balance -= Decimal(quantity * price_with_discount)
    provider.balance += Decimal(quantity * price_with_discount)

    if not ShowroomPurchase.objects.filter(showroom=showroom, provider=provider):
        provider.showroom_quantity += 1

    showroom_purchase, created = ShowroomPurchase.objects.get_or_create(
        showroom=showroom,
        provider=provider,
        model=model,
        quantity=quantity,
    )
    showroom_purchase.amount = Decimal(quantity * price_with_discount)
    showroom_car.showroom_price = price_with_discount * Decimal(os.getenv('SHOWROOM_PERCENT'))
    showroom_car.quantity += quantity

    showroom.save()
    provider.save()
    showroom_purchase.save()
    showroom_car.save()
