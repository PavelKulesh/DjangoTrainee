from car_showroom.views import BaseModelViewSet
from .serializers import CarModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import CarModelFilter


class CarModelViewSet(BaseModelViewSet):
    serializer_class = CarModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CarModelFilter
    ordering_fields = ['issue_year', 'engine_power']
    search_fields = ['name', 'brand']
