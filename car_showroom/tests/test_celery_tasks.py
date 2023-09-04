import os
from _decimal import Decimal, ROUND_DOWN
import pytest
from django.db import transaction
from django.db.models import Count
from django.utils import timezone
from django_dynamic_fixture import G
from showroom.models import Showroom, ShowroomCarCharacteristics
from showroom.models import ShowroomCar, ShowroomDiscount
from customer.utils import get_cheapest_showroom_car, get_individual_discount, get_price_with_discount, \
    process_successful_purchase
from customer.models import CustomerOffer, CustomerPurchase
from showroom.utils import get_filtered_cars, update_showroom_car
from provider.models import Provider, ProviderCar
from car.models import CarModel
from showroom.tasks import profitability_check


@pytest.mark.django_db
def test_get_cheapest_showroom_car(provider, car_model):
    showroom1 = G(Showroom)
    showroom2 = G(Showroom)

    showroom_car1 = G(ShowroomCar, provider=provider, quantity=5)
    showroom_car2 = G(ShowroomCar, provider=provider, quantity=5)

    showroom_car1.showroom = showroom1
    showroom_car2.showroom = showroom2

    showroom_car1.showroom_price = 10000
    showroom_car2.showroom_price = 9000

    showroom_car1.model = car_model
    showroom_car2.model = car_model

    showroom_car1.save()
    showroom_car2.save()

    showroom_discount = ShowroomDiscount.objects.create(
        showroom=showroom_car1.showroom,
        percent=20,
        start_at=timezone.now() - timezone.timedelta(days=1),
        end_at=timezone.now() + timezone.timedelta(days=1),
        is_active=True
    )

    showroom_discount.model_list.add(car_model)
    cheapest_car = get_cheapest_showroom_car(car_model)

    assert cheapest_car.final_price == 8000
    assert cheapest_car.showroom == showroom_car1.showroom
    assert cheapest_car.is_active == True


@pytest.mark.django_db
def test_get_individual_discount(user, showroom):
    purchases = G(CustomerPurchase, customer=user, showroom=showroom, n=10)
    percent = get_individual_discount(user, showroom)
    assert percent == 5


@pytest.mark.django_db
def test_get_price_with_discount(showroom_car, car_model):
    individual_discount = 5
    showroom_car.max_discount = 5
    showroom_car.showroom_price = 10000
    showroom_car.save()

    final_price = get_price_with_discount(individual_discount, showroom_car)

    assert Decimal(final_price).quantize(Decimal("0.01"), rounding=ROUND_DOWN) == 9000


@pytest.mark.django_db
@pytest.mark.usefixtures("disable_offer_signal")
def test_process_successful_purchase(showroom, user, car_model):
    showroom, customer, car_model = showroom, user, car_model

    customer.balance = 10000
    customer.is_confirmed = True
    customer.save()

    offer = G(CustomerOffer, customer=customer, max_price=6000)
    offer.model = car_model
    offer.save()

    showroom_car = G(ShowroomCar, showroom=showroom, showroom_price=5000, quantity=2)
    showroom_car.model = car_model
    showroom_car.save()

    with transaction.atomic():
        process_successful_purchase(offer, showroom, customer, showroom_car, 5000, car_model)

    showroom.refresh_from_db()
    customer.refresh_from_db()
    showroom_car.refresh_from_db()

    assert showroom.balance == 5000
    assert customer.balance == 5000
    assert showroom_car.quantity == 1

    customer_purchase = CustomerPurchase.objects.get(customer=customer, showroom=showroom, model=car_model)
    assert customer_purchase is not None

    assert offer.is_active == False


@pytest.mark.django_db
@pytest.mark.usefixtures("disable_charact_signal")
def test_filtered_cars(car_model):
    invalid_cars = G(CarModel, n=5)
    showroom_car_charact = G(ShowroomCarCharacteristics, brand=car_model.brand, fuel=car_model.fuel_type,
                             transmission=car_model.transmission, is_active=True)

    filtered_cars = get_filtered_cars(showroom_car_charact)

    assert filtered_cars is not None
    assert car_model in filtered_cars


@pytest.mark.django_db
def test_update_showroom_car(showroom, car_model, provider):
    provider_car = G(ProviderCar, provider=provider)
    provider_car.final_price = 10000
    provider_car.save()

    showroom_car = G(ShowroomCar, showroom=showroom, provider=provider)
    showroom_car.model = car_model
    showroom_car.save()

    update_showroom_car(showroom, car_model, provider_car)

    showroom_car.refresh_from_db()

    assert showroom_car.showroom_price == float(os.getenv('SHOWROOM_PERCENT')) * 10000


@pytest.mark.django_db
def test_annotate_from_buy_car_from_provider(showroom, car_model, user, provider):
    different_cars = G(ShowroomCar, showroom=showroom, n=10)

    purchases = G(CustomerPurchase, customer=user, showroom=showroom, n=5)
    for purch in purchases:
        purch.model = car_model
        purch.save()

    showroom_car = G(ShowroomCar, showroom=showroom, provider=provider)
    showroom_car.model = car_model
    showroom_car.save()

    showroom_cars = ShowroomCar.objects.annotate(
        num_sales=Count('model__customerpurchase')
    ).order_by('-num_sales')

    assert showroom_cars.first() == showroom_car


@pytest.mark.django_db
def test_profitability_check(car_model):
    provider1 = G(Provider)
    provider_car1 = G(ProviderCar, provider=provider1, provider_price=10000)
    provider_car1.model = car_model
    provider_car1.save()

    provider2 = G(Provider)
    provider_car2 = G(ProviderCar, provider=provider2, provider_price=90000)
    provider_car2.model = car_model
    provider_car2.save()

    showroom_car = G(ShowroomCar, provider=provider1, is_active=True)
    showroom_car.model = car_model
    showroom_car.save()

    profitability_check()

    showroom_car.refresh_from_db()

    assert showroom_car.provider == provider1
