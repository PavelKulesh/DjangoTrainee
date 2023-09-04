from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from car_showroom.models import BaseModel, BaseDiscount, BaseCarCharacteristics
from car.models import CarModel
from provider.models import Provider


class Showroom(BaseModel):
    name = models.CharField(max_length=50)
    location = CountryField(default='US')
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    model_list = models.ManyToManyField(CarModel, through='ShowroomCar')
    discount_percent = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], default=5)
    quantity_for_discount = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'showrooms'
        verbose_name = 'Showroom'
        verbose_name_plural = 'Showrooms'
        ordering = ['-updated_at']


class ShowroomCarCharacteristics(BaseModel):
    showroom = models.ForeignKey(Showroom, on_delete=models.RESTRICT)
    brand = models.CharField(max_length=20, choices=BaseCarCharacteristics.BRAND_CHOICES, null=True)
    fuel = models.CharField(max_length=20, choices=BaseCarCharacteristics.FUEL_TYPE_CHOICES, null=True)
    transmission = models.CharField(max_length=20, choices=BaseCarCharacteristics.TRANSMISSION_CHOICES, null=True)

    def __str__(self):
        return f'Charact of {self.showroom}'

    class Meta:
        db_table = 'sr_car_charact'
        verbose_name = 'SR_Charact'
        verbose_name_plural = 'SR_Characts'
        ordering = ['-updated_at']


class ShowroomCar(BaseModel):
    showroom = models.ForeignKey(Showroom, on_delete=models.RESTRICT, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.RESTRICT, null=True, blank=True)
    showroom_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'Car {self.model} of show {self.showroom}'

    class Meta:
        db_table = 'sr_car'
        verbose_name = 'SR_Car'
        verbose_name_plural = 'SR_Cars'
        ordering = ['-updated_at']


class ShowroomPurchase(BaseModel):
    showroom = models.ForeignKey(Showroom, on_delete=models.RESTRICT, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.RESTRICT, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Pur {self.model} of show {self.showroom}'

    class Meta:
        db_table = 'sr_purchases'
        verbose_name = 'SR_Purchase'
        verbose_name_plural = 'SR_Purchases'
        ordering = ['-updated_at']


class ShowroomDiscount(BaseModel, BaseDiscount):
    showroom = models.ForeignKey(Showroom, on_delete=models.RESTRICT, null=True)
    model_list = models.ManyToManyField(CarModel)

    def __str__(self):
        return f'Disc {self.pk} of show {self.showroom}'

    class Meta:
        db_table = 'sr_discounts'
        verbose_name = 'SR_Discount'
        verbose_name_plural = 'SR_Discounts'
        ordering = ['-updated_at']
