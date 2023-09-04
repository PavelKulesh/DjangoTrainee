from django.contrib.auth.models import Group, Permission
from django_filters import rest_framework as filters
from car.models import CarModel
from showroom.models import Showroom
from .models import Customer, CustomerOffer, CustomerPurchase


class CustomerFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='icontains')
    is_confirmed = filters.BooleanFilter()
    groups = filters.ModelMultipleChoiceFilter(queryset=Group.objects.all())
    user_permissions = filters.ModelMultipleChoiceFilter(queryset=Permission.objects.all())

    class Meta:
        model = Customer
        fields = ['email', 'is_confirmed', 'groups', 'user_permissions']


class CustomerOfferFilter(filters.FilterSet):
    customer = filters.ModelChoiceFilter(queryset=Customer.objects.filter(is_active=True))
    max_price = filters.RangeFilter()
    model = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.filter(is_active=True))

    class Meta:
        model = CustomerOffer
        fields = ['customer', 'max_price', 'model']


class CustomerPurchaseFilter(filters.FilterSet):
    customer = filters.ModelChoiceFilter(queryset=Customer.objects.filter(is_active=True))
    showroom = filters.ModelChoiceFilter(queryset=Showroom.objects.filter(is_active=True))
    model = filters.ModelMultipleChoiceFilter(queryset=CarModel.objects.filter(is_active=True))
    price = filters.RangeFilter()

    class Meta:
        model = CustomerPurchase
        fields = ['customer', 'showroom', 'model', 'price']
