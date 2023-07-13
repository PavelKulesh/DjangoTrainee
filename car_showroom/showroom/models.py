from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from common.models import BaseModel, BaseDiscount, BaseCarCharacteristics, CarModel
from provider.models import ProviderModel


class ShowroomModel(BaseModel):
    name = models.CharField(max_length=50)
    location = CountryField(default='US')
    balance = models.FloatField(validators=[MinValueValidator(0)], default=0)
    car_list = models.ManyToManyField(CarModel, through='ShowroomCar')
    discount_percent = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], default=5)
    quantity_for_discount = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'showrooms'
        verbose_name = 'Showroom'
        verbose_name_plural = 'Showrooms'
        ordering = ['-updated_at']


class ShowroomCarCharacteristics(BaseModel, BaseCarCharacteristics):
    showroom = models.ForeignKey(ShowroomModel, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'Char {self.pk} of {self.showroom.name}'

    class Meta:
        db_table = 'sr_characteristics'
        verbose_name = 'SR_Characteristic'
        verbose_name_plural = 'SR_Characteristics'
        ordering = ['-updated_at']


class ShowroomCar(BaseModel):
    showroom = models.ForeignKey(ShowroomModel, on_delete=models.RESTRICT, null=True)
    car = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)
    provider = models.ForeignKey(ProviderModel, on_delete=models.RESTRICT, null=True, blank=True)
    showroom_price = models.FloatField(validators=[MinValueValidator(0)], default=0)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'Car {self.car.name} of show {self.showroom.name}'

    class Meta:
        db_table = 'sr_car'
        verbose_name = 'SR_Car'
        verbose_name_plural = 'SR_Cars'
        ordering = ['-updated_at']


class ShowroomPurchase(BaseModel):
    showroom = models.ForeignKey(ShowroomModel, on_delete=models.RESTRICT, null=True)
    provider = models.ForeignKey(ProviderModel, on_delete=models.RESTRICT, null=True)
    car = models.ForeignKey(CarModel, on_delete=models.RESTRICT, null=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Pur {self.car.name} of {self.showroom.name}'

    class Meta:
        db_table = 'sr_purchases'
        verbose_name = 'SR_Purchase'
        verbose_name_plural = 'SR_Purchases'
        ordering = ['-updated_at']


class ShowroomDiscount(BaseModel, BaseDiscount):
    showroom = models.ForeignKey(ShowroomModel, on_delete=models.RESTRICT, null=True)
    car_list = models.ManyToManyField(CarModel)

    def __str__(self):
        return f'Disc {self.pk} of prov {self.showroom.name}'

    class Meta:
        db_table = 'sr_discounts'
        verbose_name = 'SR_Discount'
        verbose_name_plural = 'SR_Discounts'
        ordering = ['-updated_at']
