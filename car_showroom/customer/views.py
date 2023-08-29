from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import validate_email
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from car_showroom.permissions import IsSuperUserOrOwner, IsSuperUserOrOwnerReadOnly, IsSuperUserOrOwnerAndEmailConfirmed
from .serializers import CustomerSerializer, CustomerPurchaseSerializer, CustomerOfferSerializer
from .models import Customer, CustomerPurchase, CustomerOffer
from .services import get_data_for_serializer, login, refresh_token, generate_confirmation_url, send_confirmation_email, \
    get_customer, confirm_customer, generate_reset_url, send_reset_email, generate_change_url, send_change_email
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import CustomerFilter, CustomerOfferFilter, CustomerPurchaseFilter


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsSuperUserOrOwner]
    allowed_fields = ['first_name', 'last_name', 'username', 'email', 'password']
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CustomerFilter
    ordering_fields = ['balance']
    search_fields = ['username', 'first_name', 'last_name']

    def get_queryset(self):
        queryset = Customer.objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(Q(id=self.request.user.id) & Q(is_active=True))

        return queryset

    def create(self, request, *args, **kwargs):
        data = get_data_for_serializer(self, request)

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            customer = serializer.save()

            confirmation_url = generate_confirmation_url(customer)
            send_confirmation_email(customer, confirmation_url)

            return Response({'message': 'User registered successfully. Please check your email for confirmation.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)')
    def confirm_account(self, request, uidb64, token):
        try:
            customer = get_customer(uidb64)
            if default_token_generator.check_token(customer, token):
                confirm_customer(customer)
                return Response({'message': 'Account confirmed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid confirmation link.'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'])
    def change_password(self, request):
        customer = self.request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if customer.check_password(old_password):
            try:
                validate_password(new_password, customer)
            except ValidationError as e:
                return Response({'message': e.messages}, status=status.HTTP_400_BAD_REQUEST)

            customer.set_password(new_password)
            customer.save()
        else:
            return Response({'message': 'Wrong old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def request_password_reset(self, request):
        email = request.data.get('email')

        try:
            customer = Customer.objects.get(email=email)
            reset_url = generate_reset_url(customer)
            send_reset_email(customer, reset_url)

            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Customer not found.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='password-reset/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)')
    def password_reset(self, request, uidb64, token):
        try:
            customer = get_customer(uidb64)
            if default_token_generator.check_token(customer, token):
                new_password = request.data.get('new_password')

                try:
                    validate_password(new_password, customer)
                except ValidationError as e:
                    return Response({'message': e.messages}, status=status.HTTP_400_BAD_REQUEST)

                customer.set_password(new_password)
                customer.save()
                return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'Customer not found.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'])
    def request_email_change(self, request):
        customer = request.user

        change_url = generate_change_url(customer)
        send_change_email(customer, change_url)

        return Response({'message': 'Email change letter sent.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PATCH'], url_path='email-change/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)')
    def email_change(self, request, uidb64, token):
        try:
            customer = get_customer(uidb64)
            if default_token_generator.check_token(customer, token):
                new_email = request.data.get('new_email')

                try:
                    validate_email(new_email)
                except ValidationError as e:
                    return Response({'message': e.messages}, status=status.HTTP_400_BAD_REQUEST)

                customer.email = new_email
                customer.save()
                return Response({'message': 'Email change successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'Customer not found.'}, status=status.HTTP_400_BAD_REQUEST)


class CustomerPurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerPurchaseSerializer
    permission_classes = [IsSuperUserOrOwnerReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = CustomerPurchaseFilter
    ordering_fields = ['price']

    def get_queryset(self):
        queryset = CustomerPurchase.objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(Q(customer_id=self.request.user.id) & Q(is_active=True))

        return queryset


class CustomerOfferViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerOfferSerializer
    permission_classes = [IsSuperUserOrOwnerAndEmailConfirmed]
    allowed_fields = ['model', 'max_price']
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = CustomerOfferFilter
    ordering_fields = ['max_price']

    def get_queryset(self):
        queryset = CustomerOffer.objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(Q(customer_id=self.request.user.id) & Q(is_active=True))

        return queryset

    def create(self, request, *args, **kwargs):
        data = get_data_for_serializer(self, request)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if request.user.balance >= serializer.validated_data['max_price']:
            serializer.validated_data['customer_id'] = request.user.id
            serializer.save()
        else:
            return Response({'message': 'Not enough money'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_data_for_serializer(self, request)

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        if request.user.balance >= serializer.validated_data['max_price']:
            serializer.save()
        else:
            return Response({'message': 'Not enough money'}, status=status.HTTP_400_BAD_REQUEST)

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
