from rest_framework import serializers
from car_showroom.serializers import BaseModelSerializer
from .models import Customer, CustomerPurchase, CustomerOffer


class CustomerSerializer(BaseModelSerializer):
    private_fields = ['last_login', 'is_superuser', 'is_staff', 'is_active', 'created_at', 'groups',
                      'user_permissions']
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        customer = Customer.objects.create(**validated_data)

        if password:
            customer.set_password(password)
            customer.save()

        return customer

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


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
