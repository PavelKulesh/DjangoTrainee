from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AuthViewSet, CustomerViewSet, CustomerPurchaseViewSet, CustomerOfferViewSet, \
    CustomerStatisticsViewSet

router = SimpleRouter()

router.register(r'login', AuthViewSet, basename='auth')
router.register(r'purchase', CustomerPurchaseViewSet, basename='customer-purchase')
router.register(r'offer', CustomerOfferViewSet, basename='customer-offer')
router.register(r'statistics', CustomerStatisticsViewSet, basename='customer-statistics')
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
