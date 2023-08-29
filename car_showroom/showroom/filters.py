import django_countries
from django_filters import rest_framework as filters
from car.models import CarModel
from provider.models import Provider
from .models import Showroom, ShowroomCarCharacteristics, ShowroomCar, ShowroomPurchase, ShowroomDiscount


class ShowroomFilter(filters.FilterSet):
    location = filters.ChoiceFilter(choices=django_countries.countries)
    model_list = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.all())
    discount_percent = filters.RangeFilter()
    quantity_for_discount = filters.RangeFilter()

    class Meta:
        model = Showroom
        fields = ['location', 'model_list', 'discount_percent', 'quantity_for_discount']


class ShowroomCarCharacteristicsFilter(filters.FilterSet):
    showroom = filters.ModelChoiceFilter(queryset=Showroom.objects.all())
    brand = filters.MultipleChoiceFilter(choices=CarModel.BRAND_CHOICES)
    fuel = filters.MultipleChoiceFilter(choices=CarModel.FUEL_TYPE_CHOICES)
    transmission = filters.MultipleChoiceFilter(choices=CarModel.TRANSMISSION_CHOICES)

    class Meta:
        model = ShowroomCarCharacteristics
        fields = ['showroom', 'brand', 'fuel', 'transmission']


class ShowroomCarFilter(filters.FilterSet):
    showroom = filters.ModelChoiceFilter(queryset=Showroom.objects.all())
    model = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.all())
    provider = filters.ModelMultipleChoiceFilter(queryset=Provider.objects.all())
    showroom_price = filters.RangeFilter()
    quantity = filters.RangeFilter()

    class Meta:
        model = ShowroomCar
        fields = ['showroom', 'model', 'provider', 'showroom_price', 'quantity']


class ShowroomPurchaseFilter(filters.FilterSet):
    showroom = filters.ModelChoiceFilter(queryset=Showroom.objects.all())
    provider = filters.ModelMultipleChoiceFilter(queryset=Provider.objects.all())
    model = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.all())
    quantity = filters.RangeFilter()
    amount = filters.RangeFilter()

    class Meta:
        model = ShowroomPurchase
        fields = ['showroom', 'provider', 'model', 'quantity', 'amount']


class ShowroomDiscountFilter(filters.FilterSet):
    start_at = filters.DateFilter(lookup_expr='gte')
    end_at = filters.DateFilter(lookup_expr='lte')
    showroom = filters.ModelChoiceFilter(queryset=Showroom.objects.all())
    model_list = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.all())

    class Meta:
        model = ShowroomDiscount
        fields = ['start_at', 'end_at', 'showroom', 'model_list']
