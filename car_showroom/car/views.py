from car_showroom.views import BaseModelViewSet
from .serializers import CarModelSerializer


class CarModelViewSet(BaseModelViewSet):
    serializer_class = CarModelSerializer
