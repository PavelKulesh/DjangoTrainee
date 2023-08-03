from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CarModelViewSet

router = SimpleRouter()

router.register(r'', CarModelViewSet, basename='car-model')

urlpatterns = [
    path('', include(router.urls))
]
