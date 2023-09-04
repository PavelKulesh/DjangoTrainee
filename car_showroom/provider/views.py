from car_showroom.views import BaseModelViewSet
from .serializers import ProviderSerializer, ProviderCarSerializer, ProviderDiscountSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProviderFilter, ProviderCarFilter, ProviderDiscountFilter


class ProviderViewSet(BaseModelViewSet):
    serializer_class = ProviderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProviderFilter
    ordering_fields = ['foundation_year', 'showroom_quantity', 'balance', 'discount_percent', 'quantity_for_discount']
    search_fields = ['name']


class ProviderCarViewSet(BaseModelViewSet):
    serializer_class = ProviderCarSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProviderCarFilter
    ordering_fields = ['provider_price']


class ProviderDiscountViewSet(BaseModelViewSet):
    serializer_class = ProviderDiscountSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProviderDiscountFilter
    ordering_fields = ['percent']
    search_fields = ['name']
