from django.contrib import admin
from .models import Customer, CustomerPurchase, CustomerOffer

admin.site.register(Customer)
admin.site.register(CustomerPurchase)
admin.site.register(CustomerOffer)
