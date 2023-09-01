from rest_framework.permissions import IsAdminUser
from car_showroom.views import BaseModelViewSet
from .serializers import ShowroomSerializer, ShowroomCarCharacteristicsSerializer, ShowroomCarSerializer, \
    ShowroomDiscountSerializer, ShowroomPurchaseSerializer


class ShowroomViewSet(BaseModelViewSet):
    serializer_class = ShowroomSerializer


class ShowroomCarCharacteristicsViewSet(BaseModelViewSet):
    serializer_class = ShowroomCarCharacteristicsSerializer
    permission_classes = [IsAdminUser]


class ShowroomCarViewSet(BaseModelViewSet):
    serializer_class = ShowroomCarSerializer


class ShowroomDiscountViewSet(BaseModelViewSet):
    serializer_class = ShowroomDiscountSerializer


class ShowroomPurchaseViewSet(BaseModelViewSet):
    serializer_class = ShowroomPurchaseSerializer
    permission_classes = [IsAdminUser]
