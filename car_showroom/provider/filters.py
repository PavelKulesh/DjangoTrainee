from django_filters import rest_framework as filters
from car.models import CarModel
from .models import Provider, ProviderCar, ProviderDiscount


class ProviderFilter(filters.FilterSet):
    foundation_year = filters.RangeFilter()
    showroom_quantity = filters.RangeFilter()
    balance = filters.RangeFilter()
    model_list = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.filter(is_active=True))
    discount_percent = filters.RangeFilter()
    quantity_for_discount = filters.RangeFilter()

    class Meta:
        model = Provider
        fields = ['foundation_year', 'showroom_quantity', 'balance', 'model_list', 'discount_percent',
                  'quantity_for_discount']


class ProviderCarFilter(filters.FilterSet):
    provider = filters.ModelChoiceFilter(queryset=Provider.objects.filter(is_active=True))
    model = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.filter(is_active=True))
    provider_price = filters.RangeFilter()

    class Meta:
        model = ProviderCar
        fields = ['provider', 'model', 'provider_price']


class ProviderDiscountFilter(filters.FilterSet):
    start_at = filters.DateFilter(lookup_expr='gte')
    end_at = filters.DateFilter(lookup_expr='lte')
    provider = filters.ModelChoiceFilter(queryset=Provider.objects.filter(is_active=True))
    model_list = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.filter(is_active=True))

    class Meta:
        model = ProviderDiscount
        fields = ['start_at', 'end_at', 'provider', 'model_list']
