from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from car_showroom.models import BaseModel
from car.models import CarModel
from showroom.models import Showroom


class Customer(AbstractUser, BaseModel):
    is_confirmed = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-updated_at']


class CustomerPurchase(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True)
    showroom = models.ForeignKey(Showroom, on_delete=models.RESTRICT, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f'Pur {self.model} of cust {self.customer}'

    class Meta:
        db_table = 'customer_purchases'
        verbose_name = 'Customer_Purchase'
        verbose_name_plural = 'Customer_Purchases'
        ordering = ['-updated_at']


class CustomerOffer(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    model = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'Off {self.model} of cust {self.customer}'

    class Meta:
        db_table = 'customer_offers'
        verbose_name = 'Customer_Offer'
        verbose_name_plural = 'Customer_Offers'
        ordering = ['-updated_at']
