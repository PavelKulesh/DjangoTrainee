import random
import string
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django_countries import countries
from car.models import CarModel
from provider.models import Provider, ProviderCar, ProviderDiscount
from showroom.models import Showroom, ShowroomCarCharacteristics

BRAND_CHOICES = [
    'Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes-Benz', 'Audi', 'Chevrolet', 'Volkswagen',
    'Hyundai', 'Nissan', 'Kia', 'Volvo', 'Subaru', 'Mazda', 'Lexus', 'Tesla', 'Porsche',
    'Jeep', 'Land Rover', 'Ferrari', 'Lamborghini', 'Maserati', 'Bentley',
]

BODY_TYPE_CHOICES = ['Sedan', 'Hatchback', 'Crossover', 'Coupe', 'Jeep']

FUEL_TYPE_CHOICES = ['Petrol', 'Diesel', 'Biodiesel', 'Propane', 'Electricity']

TRANSMISSION_CHOICES = ['Mechanical', 'Automatic', 'Variator']

DRIVE_UNIT_CHOICES = ['Front', 'Rear', 'All']


def generate_random_car_data():
    car_data = {
        'name': generate_random_string(10),
        'brand': random.choice(BRAND_CHOICES),
        'issue_year': random.randint(2000, 2023),
        'body_type': random.choice(BODY_TYPE_CHOICES),
        'engine_capacity': Decimal(random.uniform(1.0, 5.0)),
        'engine_power': random.randint(100, 500),
        'fuel_type': random.choice(FUEL_TYPE_CHOICES),
        'transmission': random.choice(TRANSMISSION_CHOICES),
        'drive_unit': random.choice(DRIVE_UNIT_CHOICES),
    }
    return car_data


def generate_random_provider_data():
    provider_data = {
        'name': generate_random_string(10),
        'foundation_year': random.randint(1900, 2023),
        'showroom_quantity': 0,
        'balance': 0,
        'discount_percent': random.randint(0, 50),
        'quantity_for_discount': random.randint(5, 50),
    }
    return provider_data


def generate_random_provider_car_data(providers, car_models):
    while True:
        provider = random.choice(providers)
        car_model = random.choice(car_models)

        if not ProviderCar.objects.filter(provider=provider, model=car_model).exists():
            break

    provider_car_data = {
        'provider': provider,
        'model': car_model,
        'provider_price': Decimal(random.uniform(1000, 50000)),
    }
    return provider_car_data


def generate_random_showroom_data():
    showroom_data = {
        'name': generate_random_string(10),
        'location': random.choice(countries),
        'balance': Decimal(random.uniform(10000, 100000)),
        'discount_percent': random.randint(1, 50),
        'quantity_for_discount': random.randint(5, 20),
    }
    return showroom_data


def generate_random_showroom_car_characts(showroom):
    showroom_car_characts = {
        'showroom': showroom,
        'brand': random.choice(BRAND_CHOICES),
        'fuel': random.choice(FUEL_TYPE_CHOICES),
        'transmission': random.choice(TRANSMISSION_CHOICES),
    }
    return showroom_car_characts


def generate_random_string(length):
    return (''.join(random.choice(string.ascii_letters) for _ in range(length))).capitalize()


def generate_random_provider_discount_data(provider):
    provider_cars = ProviderCar.objects.filter(provider=provider)
    random_cars = random.sample(list(provider_cars), min(3, provider_cars.count()))
    provider_discount = ProviderDiscount.objects.create(
        provider=provider,
        start_at=timezone.now(),
        end_at=timezone.now() + timedelta(days=random.randint(7, 30)),
        name=generate_random_string(10),
        description=generate_random_string(30),
        percent=random.randint(1, 20),
    )
    for car in random_cars:
        provider_discount.model_list.add(car.model.id)


def init_db():
    num_cars = 100
    for _ in range(num_cars):
        car_data = generate_random_car_data()
        car = CarModel(**car_data)
        car.save()

    num_providers = 20
    for _ in range(num_providers):
        provider_data = generate_random_provider_data()
        provider = Provider(**provider_data)
        provider.save()

    num_provider_cars = 100
    providers = Provider.objects.all()
    car_models = CarModel.objects.all()
    for _ in range(num_provider_cars):
        provider_car_data = generate_random_provider_car_data(providers, car_models)
        provider_car = ProviderCar(**provider_car_data)
        provider_car.save()

    num_showrooms = 30
    for _ in range(num_showrooms):
        showroom_data = generate_random_showroom_data()
        showroom = Showroom(**showroom_data)
        showroom.save()

    characts_count = 5
    showrooms = Showroom.objects.all()
    for showroom in showrooms:
        for _ in range(characts_count):
            characts = generate_random_showroom_car_characts(showroom)
            ShowroomCarCharacteristics.objects.create(**characts)

    count_discounts_for_provider = 2
    for provider in providers:
        for _ in range(count_discounts_for_provider):
            generate_random_provider_discount_data(provider)


if __name__ == '__main__':
    init_db()
