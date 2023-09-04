from django_filters import rest_framework as filters
from .models import CarModel


class CarModelFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    brand = filters.MultipleChoiceFilter(choices=CarModel.BRAND_CHOICES)
    issue_year = filters.RangeFilter()
    body_type = filters.MultipleChoiceFilter(choices=CarModel.BODY_TYPE_CHOICES)
    engine_capacity = filters.RangeFilter()
    engine_power = filters.RangeFilter()
    fuel_type = filters.MultipleChoiceFilter(choices=CarModel.FUEL_TYPE_CHOICES)
    transmission = filters.MultipleChoiceFilter(choices=CarModel.TRANSMISSION_CHOICES)
    drive_unit = filters.MultipleChoiceFilter(choices=CarModel.DRIVE_UNIT_CHOICES)

    class Meta:
        model = CarModel
        fields = ['name', 'brand', 'issue_year', 'body_type', 'engine_capacity', 'engine_power',
                  'fuel_type', 'transmission', 'drive_unit']
