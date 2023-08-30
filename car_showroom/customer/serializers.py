from rest_framework import serializers
from car_showroom.serializers import BaseModelSerializer
from car.serializers import CarModelSerializer
from .models import Customer, CustomerPurchase, CustomerOffer


class CustomerSerializer(BaseModelSerializer):
    private_fields = ['last_login', 'is_superuser', 'is_staff', 'is_active', 'created_at', 'groups',
                      'user_permissions']

    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer


class CustomerPurchaseSerializer(BaseModelSerializer):
    private_fields = ['is_active', 'updated_at']

    class Meta:
        model = CustomerPurchase
        fields = '__all__'


class CustomerOfferSerializer(BaseModelSerializer):
    private_fields = ['is_active']

    class Meta:
        model = CustomerOffer
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)


class CustomerStatisticsSerializer(serializers.Serializer):
    total_cost_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    count_of_purchases = serializers.IntegerField()
    list_of_bought_cars = CarModelSerializer(many=True)
