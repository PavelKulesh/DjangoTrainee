from django.contrib import admin
from .models import Showroom, ShowroomCarBrand, ShowroomCarFuel, ShowroomCarTransmission, ShowroomCar, ShowroomPurchase, \
    ShowroomDiscount

admin.site.register(Showroom)
admin.site.register(ShowroomCarBrand)
admin.site.register(ShowroomCarFuel)
admin.site.register(ShowroomCarTransmission)
admin.site.register(ShowroomCar)
admin.site.register(ShowroomPurchase)
admin.site.register(ShowroomDiscount)
