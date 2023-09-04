from django.contrib import admin
from .models import Showroom, ShowroomCarCharacteristics, ShowroomCar, ShowroomPurchase, ShowroomDiscount

admin.site.register(Showroom)
admin.site.register(ShowroomCarCharacteristics)
admin.site.register(ShowroomCar)
admin.site.register(ShowroomPurchase)
admin.site.register(ShowroomDiscount)
