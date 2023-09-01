from car_showroom.serializers import BaseModelSerializer
from .models import Showroom, ShowroomCarCharacteristics, ShowroomCar, ShowroomDiscount, ShowroomPurchase


class ShowroomSerializer(BaseModelSerializer):
    private_fields = ['is_active', 'created_at', 'updated_at', 'balance']

    class Meta:
        model = Showroom
        fields = '__all__'


class ShowroomCarCharacteristicsSerializer(BaseModelSerializer):
    private_fields = []

    class Meta:
        model = ShowroomCarCharacteristics
        fields = '__all__'


class ShowroomCarSerializer(BaseModelSerializer):
    class Meta:
        model = ShowroomCar
        fields = '__all__'


class ShowroomDiscountSerializer(BaseModelSerializer):
    class Meta:
        model = ShowroomDiscount
        fields = '__all__'


class ShowroomPurchaseSerializer(BaseModelSerializer):
    private_fields = []

    class Meta:
        model = ShowroomPurchase
        fields = '__all__'
