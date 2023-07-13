from django.contrib import admin
from .models import ShowroomModel, ShowroomCarCharacteristics, ShowroomCar, ShowroomPurchase, ShowroomDiscount

admin.site.register(ShowroomModel)
admin.site.register(ShowroomCarCharacteristics)
admin.site.register(ShowroomCar)
admin.site.register(ShowroomPurchase)
admin.site.register(ShowroomDiscount)
