from car_showroom.views import BaseModelViewSet
from .serializers import ProviderSerializer, ProviderCarSerializer, ProviderDiscountSerializer


class ProviderViewSet(BaseModelViewSet):
    serializer_class = ProviderSerializer


class ProviderCarViewSet(BaseModelViewSet):
    serializer_class = ProviderCarSerializer


class ProviderDiscountViewSet(BaseModelViewSet):
    serializer_class = ProviderDiscountSerializer
