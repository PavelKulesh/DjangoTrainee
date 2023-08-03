from car_showroom.serializers import BaseModelSerializer
from .models import Showroom, ShowroomCar, ShowroomDiscount, ShowroomCarBrand, ShowroomCarFuel, ShowroomCarTransmission, \
    ShowroomPurchase


class ShowroomSerializer(BaseModelSerializer):
    private_fields = ['is_active', 'created_at', 'updated_at', 'balance']

    class Meta:
        model = Showroom
        fields = '__all__'


class ShowroomCarSerializer(BaseModelSerializer):
    class Meta:
        model = ShowroomCar
        fields = '__all__'


class ShowroomDiscountSerializer(BaseModelSerializer):
    class Meta:
        model = ShowroomDiscount
        fields = '__all__'


class ShowroomCarBrandSerializer(BaseModelSerializer):
    private_fields = []

    class Meta:
        model = ShowroomCarBrand
        fields = '__all__'


class ShowroomCarFuelSerializer(BaseModelSerializer):
    private_fields = []

    class Meta:
        model = ShowroomCarFuel
        fields = '__all__'


class ShowroomCarTransmissionSerializer(BaseModelSerializer):
    private_fields = []

    class Meta:
        model = ShowroomCarTransmission
        fields = '__all__'


class ShowroomPurchaseSerializer(BaseModelSerializer):
    private_fields = []

    class Meta:
        model = ShowroomPurchase
        fields = '__all__'
