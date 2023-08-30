from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProviderViewSet, ProviderCarViewSet, ProviderDiscountViewSet, ProviderStatisticsViewSet

router = SimpleRouter()

router.register(r'car', ProviderCarViewSet, basename='provider-car')
router.register(r'discount', ProviderDiscountViewSet, basename='provider-discount')
router.register(r'statistics', ProviderStatisticsViewSet, basename='provider-statistics')
router.register(r'', ProviderViewSet, basename='provider')

urlpatterns = [
    path('', include(router.urls))
]
