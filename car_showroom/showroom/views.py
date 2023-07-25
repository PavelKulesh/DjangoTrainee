from rest_framework.permissions import IsAdminUser
from car_showroom.views import BaseModelViewSet
from .serializers import ShowroomSerializer, ShowroomCarSerializer, ShowroomDiscountSerializer, \
    ShowroomCarBrandSerializer, ShowroomCarFuelSerializer, ShowroomCarTransmissionSerializer, ShowroomPurchaseSerializer


class ShowroomViewSet(BaseModelViewSet):
    serializer_class = ShowroomSerializer


class ShowroomCarViewSet(BaseModelViewSet):
    serializer_class = ShowroomCarSerializer


class ShowroomDiscountViewSet(BaseModelViewSet):
    serializer_class = ShowroomDiscountSerializer


class ShowroomCarBrandViewSet(BaseModelViewSet):
    serializer_class = ShowroomCarBrandSerializer
    permission_classes = [IsAdminUser]


class ShowroomCarFuelViewSet(BaseModelViewSet):
    serializer_class = ShowroomCarFuelSerializer
    permission_classes = [IsAdminUser]


class ShowroomCarTransmissionViewSet(BaseModelViewSet):
    serializer_class = ShowroomCarTransmissionSerializer
    permission_classes = [IsAdminUser]


class ShowroomPurchaseViewSet(BaseModelViewSet):
    serializer_class = ShowroomPurchaseSerializer
    permission_classes = [IsAdminUser]
