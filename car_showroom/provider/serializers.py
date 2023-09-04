from rest_framework import serializers
from car_showroom.serializers import BaseModelSerializer
from car.serializers import CarModelSerializer
from .models import Provider, ProviderCar, ProviderDiscount


class ProviderSerializer(BaseModelSerializer):
    private_fields = ['is_active', 'created_at', 'updated_at', 'showroom_quantity', 'balance']

    class Meta:
        model = Provider
        fields = '__all__'


class ProviderCarSerializer(BaseModelSerializer):
    class Meta:
        model = ProviderCar
        fields = '__all__'


class ProviderDiscountSerializer(BaseModelSerializer):
    class Meta:
        model = ProviderDiscount
        fields = '__all__'


class ProviderStatisticsSerializer(serializers.Serializer):
    count_of_sales = serializers.IntegerField()
    total_cost_of_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    list_of_sold_cars = CarModelSerializer(many=True)
