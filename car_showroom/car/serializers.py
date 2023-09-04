from car_showroom.serializers import BaseModelSerializer
from .models import CarModel


class CarModelSerializer(BaseModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'
