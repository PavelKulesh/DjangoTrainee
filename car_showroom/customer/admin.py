from django.contrib import admin
from .models import CustomerModel, CustomerPurchase, CustomerOffer

admin.site.register(CustomerModel)
admin.site.register(CustomerPurchase)
admin.site.register(CustomerOffer)
