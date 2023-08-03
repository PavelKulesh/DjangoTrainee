from car_showroom.serializers import BaseModelSerializer
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
