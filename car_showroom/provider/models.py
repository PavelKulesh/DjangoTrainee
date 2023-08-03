from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from car_showroom.models import BaseModel, BaseDiscount
from car.models import CarModel


class Provider(BaseModel):
    name = models.CharField(max_length=50)
    foundation_year = models.PositiveSmallIntegerField()
    showroom_quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    model_list = models.ManyToManyField(CarModel, through='ProviderCar')
    discount_percent = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], default=5)
    quantity_for_discount = models.PositiveSmallIntegerField(default=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'providers'
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
        ordering = ['-updated_at']


class ProviderCar(BaseModel):
    provider = models.ForeignKey(Provider, on_delete=models.RESTRICT, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)
    provider_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f'Car {self.model} of prov {self.provider}'

    class Meta:
        db_table = 'provider_cars'
        verbose_name = 'Provider_Car'
        verbose_name_plural = 'Provider_Cars'
        ordering = ['-updated_at']


class ProviderDiscount(BaseModel, BaseDiscount):
    provider = models.ForeignKey(Provider, on_delete=models.RESTRICT, null=True)
    model_list = models.ManyToManyField(CarModel)

    def __str__(self):
        return f'Disc {self.pk} of prov {self.provider}'

    class Meta:
        db_table = 'provider_discounts'
        verbose_name = 'Provider_Discount'
        verbose_name_plural = 'Provider_Discounts'
        ordering = ['-updated_at']
