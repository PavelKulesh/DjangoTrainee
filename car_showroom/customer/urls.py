from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AuthViewSet

simple_router = SimpleRouter()

simple_router.register(r'login', AuthViewSet, basename='login')

urlpatterns = [
    path('', include(simple_router.urls)),
]
