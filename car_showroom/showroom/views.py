from rest_framework.permissions import IsAdminUser
from car_showroom.views import BaseModelViewSet
from .serializers import ShowroomSerializer, ShowroomCarCharacteristicsSerializer, ShowroomCarSerializer, \
    ShowroomDiscountSerializer, ShowroomPurchaseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ShowroomFilter, ShowroomCarCharacteristicsFilter, ShowroomCarFilter, ShowroomPurchaseFilter, \
    ShowroomDiscountFilter


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
