from django.db.models import Sum
from car.models import CarModel

from showroom.models import ShowroomPurchase


class ProviderStatisticsService:
    @staticmethod
    def count_of_sales(provider):
        sold_cars = ShowroomPurchase.objects.filter(provider=provider).aggregate(total_sold=Sum('quantity'))
        return sold_cars['total_sold'] or 0

    @staticmethod
    def total_cost_of_sales(provider):
        sold_cars = ShowroomPurchase.objects.filter(provider=provider).aggregate(total_amount=Sum('amount'))
        return sold_cars['total_amount'] or 0

    @staticmethod
    def list_of_sold_cars(provider):
        sold_cars = ShowroomPurchase.objects.filter(provider=provider).values_list('model', flat=True)
        car_models = CarModel.objects.filter(id__in=sold_cars)
        return car_models
