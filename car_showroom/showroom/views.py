from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets, status
from car_showroom.views import BaseModelViewSet
from .serializers import ShowroomSerializer, ShowroomCarCharacteristicsSerializer, ShowroomCarSerializer, \
    ShowroomDiscountSerializer, ShowroomPurchaseSerializer, ShowroomStatisticsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ShowroomFilter, ShowroomCarCharacteristicsFilter, ShowroomCarFilter, ShowroomPurchaseFilter, \
    ShowroomDiscountFilter
from .models import Showroom
from .services import ShowroomStatisticsService


class ShowroomViewSet(BaseModelViewSet):
    serializer_class = ShowroomSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ShowroomFilter
    ordering_fields = ['balance', 'discount_percent', 'quantity_for_discount']
    search_fields = ['name']


class ShowroomCarCharacteristicsViewSet(BaseModelViewSet):
    serializer_class = ShowroomCarCharacteristicsSerializer
    permission_classes = [IsAdminUser]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ShowroomCarCharacteristicsFilter


class ShowroomCarViewSet(BaseModelViewSet):
    serializer_class = ShowroomCarSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ShowroomCarFilter
    ordering_fields = ['showroom_price', 'quantity']


class ShowroomDiscountViewSet(BaseModelViewSet):
    serializer_class = ShowroomDiscountSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ShowroomDiscountFilter
    ordering_fields = ['percent']
    search_fields = ['name']


class ShowroomPurchaseViewSet(BaseModelViewSet):
    serializer_class = ShowroomPurchaseSerializer
    permission_classes = [IsAdminUser]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ShowroomPurchaseFilter
    ordering_fields = ['quantity', 'amount']


class ShowroomStatisticsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            showroom = Showroom.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'message': 'Showroom not found'}, status=status.HTTP_404_NOT_FOUND)

        count_of_sales = ShowroomStatisticsService.count_of_sales(showroom)
        total_cost_of_sales = ShowroomStatisticsService.total_cost_of_sales(showroom)
        count_of_unique_customers = ShowroomStatisticsService.count_of_unique_customers(showroom)

        serializer = ShowroomStatisticsSerializer(
            {
                'count_of_sales': count_of_sales,
                'total_cost_of_sales': total_cost_of_sales,
                'count_of_unique_customers': count_of_unique_customers,
            },
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
