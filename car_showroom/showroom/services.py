from django.db.models import Sum, Count

from customer.models import CustomerPurchase


class ShowroomStatisticsService:
    @staticmethod
    def count_of_sales(showroom):
        return CustomerPurchase.objects.filter(showroom=showroom).count()

    @staticmethod
    def total_cost_of_sales(showroom):
        sales = CustomerPurchase.objects.filter(showroom=showroom).aggregate(total_amount=Sum('price'))
        return sales['total_amount'] or 0

    @staticmethod
    def count_of_unique_customers(showroom):
        return CustomerPurchase.objects.filter(showroom=showroom).values('customer').annotate(
            num_purchases=Count('customer')).count()
