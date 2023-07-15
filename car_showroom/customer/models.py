from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from common.models import BaseModel, CarModel
from showroom.models import ShowroomModel


class CustomerModel(AbstractUser, BaseModel):
    is_confirmed = models.BooleanField(default=False)
    balance = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-updated_at']


class CustomerPurchase(BaseModel):
    customer = models.ForeignKey(CustomerModel, on_delete=models.RESTRICT, null=True)
    showroom = models.ForeignKey(ShowroomModel, on_delete=models.RESTRICT, null=True)
    car = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)
    price = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f'Pur {self.car.name} of cust {self.customer}'

    class Meta:
        db_table = 'customer_purchases'
        verbose_name = 'Customer_Purchase'
        verbose_name_plural = 'Customer_Purchases'
        ordering = ['-updated_at']


class CustomerOffer(BaseModel):
    customer = models.ForeignKey(CustomerModel, on_delete=models.RESTRICT, null=True)
    max_price = models.FloatField(validators=[MinValueValidator(0)], default=0)
    car = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'Off {self.car.name} of cust {self.customer}'

    class Meta:
        db_table = 'customer_offers'
        verbose_name = 'Customer_Offer'
        verbose_name_plural = 'Customer_Offers'
        ordering = ['-updated_at']
