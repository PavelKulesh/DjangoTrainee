from django.contrib import admin
from .models import ProviderModel, ProviderCar, ProviderDiscount

admin.site.register(ProviderModel)
admin.site.register(ProviderCar)
admin.site.register(ProviderDiscount)
