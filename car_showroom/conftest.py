import pytest
from django_dynamic_fixture import G
from car.models import CarModel
from customer.models import Customer, CustomerOffer
from showroom.models import Showroom, ShowroomCar
from provider.models import Provider


@pytest.fixture
def user():
    user = Customer.objects.create_user(
        username='valid_username',
        email='valid_email',
        password='valid_password',
    )

    return user


@pytest.fixture
def car_model():
    car_model = CarModel.objects.create(
        name='S63 AMG',
        brand='Mercedes-Benz',
        issue_year=2018,
        body_type='Sedan',
        engine_capacity=4.0,
        engine_power=612,
        fuel_type='Petrol',
        transmission='Automatic',
        drive_unit='All',
    )

    return car_model


@pytest.fixture
def showroom():
    return G(Showroom, quantity_for_discount=10, discount_percent=5)


@pytest.fixture
def provider():
    provider = Provider.objects.create(
        name='TestProvider',
        foundation_year=2010,
    )

    return provider


@pytest.fixture
def showroom_car(provider):
    return G(ShowroomCar, provider=provider, quantity=5)


@pytest.fixture
def disable_offer_signal(mocker):
    mocker.patch("customer.signals.buy_offered_car.delay")


@pytest.fixture
def disable_charact_signal(mocker):
    mocker.patch("showroom.signals.get_showroom_cars.delay")
