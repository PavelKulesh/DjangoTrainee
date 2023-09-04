from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import viewsets, status
from car_showroom.views import BaseModelViewSet
from .serializers import ProviderSerializer, ProviderCarSerializer, ProviderDiscountSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProviderFilter, ProviderCarFilter, ProviderDiscountFilter
from .models import Provider
from .services import ProviderStatisticsService
from .serializers import ProviderStatisticsSerializer


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


class ProviderStatisticsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            provider = Provider.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'message': 'Provider not found'}, status=status.HTTP_404_NOT_FOUND)

        count_of_sales = ProviderStatisticsService.count_of_sales(provider)
        total_cost_of_sales = ProviderStatisticsService.total_cost_of_sales(provider)
        list_of_sold_cars = ProviderStatisticsService.list_of_sold_cars(provider)

        serializer = ProviderStatisticsSerializer(
            {
                'count_of_sales': count_of_sales,
                'total_cost_of_sales': total_cost_of_sales,
                'list_of_sold_cars': list_of_sold_cars,
            },
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
