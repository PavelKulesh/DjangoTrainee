import pytest
from car.models import CarModel


@pytest.mark.django_db
def test_soft_delete():
    car = CarModel(
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
    car.save()

    assert car.is_active is True

    initial_created_at = car.created_at
    initial_updated_at = car.updated_at

    car.delete()

    deleted_car = CarModel.objects.get(id=car.id)

    assert deleted_car.is_active is False
    assert deleted_car.created_at == initial_created_at
    assert deleted_car.updated_at > initial_updated_at
