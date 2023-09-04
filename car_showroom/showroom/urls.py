from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ShowroomViewSet, ShowroomCarCharacteristicsViewSet, ShowroomCarViewSet, ShowroomDiscountViewSet, \
    ShowroomPurchaseViewSet, ShowroomStatisticsViewSet

router = SimpleRouter()

router.register(r'car', ShowroomCarViewSet, basename='showroom-car')
router.register(r'discount', ShowroomDiscountViewSet, basename='showroom-discount')
router.register(r'characteristics', ShowroomCarCharacteristicsViewSet, basename='showroom-car-characteristics')
router.register(r'purchase', ShowroomPurchaseViewSet, basename='showroom-purchase')
router.register(r'statistics', ShowroomStatisticsViewSet, basename='showroom-statistics')
router.register(r'', ShowroomViewSet, basename='showroom')

urlpatterns = [
    path('', include(router.urls))
]
