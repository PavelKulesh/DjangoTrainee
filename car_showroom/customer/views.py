from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from car_showroom.permissions import IsSuperUserOrOwner, IsSuperUserOrOwnerReadOnly, IsSuperUserOrOwnerAndEmailConfirmed
from .serializers import CustomerSerializer, CustomerPurchaseSerializer, CustomerOfferSerializer
from .models import Customer, CustomerPurchase, CustomerOffer
from .services import get_data_for_serializer, login, refresh_token


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsSuperUserOrOwner]
    allowed_fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def get_queryset(self):
        queryset = Customer.objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(Q(id=self.request.user.id) & Q(is_active=True))

        return queryset

    def create(self, request, *args, **kwargs):
        data = get_data_for_serializer(self, request)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_data_for_serializer(self, request)

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'email' in data and data['email'] != instance.email:
            serializer.validated_data['is_confirmed'] = False

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerPurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerPurchaseSerializer
    permission_classes = [IsSuperUserOrOwnerReadOnly]

    def get_queryset(self):
        queryset = CustomerPurchase.objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(Q(customer_id=self.request.user.id) & Q(is_active=True))

        return queryset


class CustomerOfferViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerOfferSerializer
    permission_classes = [IsSuperUserOrOwnerAndEmailConfirmed]
    allowed_fields = ['model', 'max_price']

    def get_queryset(self):
        queryset = CustomerOffer.objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(Q(customer_id=self.request.user.id) & Q(is_active=True))

        return queryset

    def create(self, request, *args, **kwargs):
        data = get_data_for_serializer(self, request)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['customer_id'] = request.user.id
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_data_for_serializer(self, request)

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        action = request.data.get('action')

        if action == 'login':
            return login(request)
        elif action == 'refresh':
            return refresh_token(request)
        else:
            return Response({'error': 'Invalid action! Choose login or refresh.'}, status=status.HTTP_400_BAD_REQUEST)
