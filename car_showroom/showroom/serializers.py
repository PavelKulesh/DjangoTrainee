from rest_framework import serializers
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


class ShowroomStatisticsSerializer(serializers.Serializer):
    count_of_sales = serializers.IntegerField()
    total_cost_of_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    count_of_unique_customers = serializers.IntegerField()
