from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ShowroomViewSet, ShowroomCarViewSet, ShowroomDiscountViewSet, ShowroomCarBrandViewSet, \
    ShowroomCarFuelViewSet, ShowroomCarTransmissionViewSet, ShowroomPurchaseViewSet

router = SimpleRouter()

router.register(r'car', ShowroomCarViewSet, basename='showroom-car')
router.register(r'discount', ShowroomDiscountViewSet, basename='showroom-discount')
router.register(r'brand', ShowroomCarBrandViewSet, basename='showroom-car-brand')
router.register(r'fuel', ShowroomCarFuelViewSet, basename='showroom-car-fuel')
router.register(r'transmission', ShowroomCarTransmissionViewSet, basename='showroom-car-transmission')
router.register(r'purchase', ShowroomPurchaseViewSet, basename='showroom-purchase')
router.register(r'', ShowroomViewSet, basename='showroom')

urlpatterns = [
    path('', include(router.urls))
]
