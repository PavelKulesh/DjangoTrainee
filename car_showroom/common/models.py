from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseDiscount(models.Model):
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    percent = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], default=5)

    class Meta:
        abstract = True


class BaseCarCharacteristics(models.Model):
    BODY_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
        ('Crossover', 'Crossover'),
        ('Coupe', 'Coupe'),
        ('Jeep', 'Jeep'),
    ]

    FUEL_TYPE_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Biodiesel', 'Biodiesel'),
        ('Propane', 'Propane'),
        ('Electricity', 'Electricity'),
    ]

    TRANSMISSION_CHOICES = [
        ('Mechanical', 'Mechanical'),
        ('Automatic', 'Automatic'),
        ('Variator', 'Variator'),
    ]

    DRIVE_UNIT_CHOICES = [
        ('Front', 'Front'),
        ('Rear', 'Rear'),
        ('All', 'All'),
    ]

    issue_year = models.PositiveSmallIntegerField(default=2010)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES)
    engine_capacity = models.FloatField(validators=[MinValueValidator(0)], default=0)
    engine_power = models.PositiveIntegerField(default=0)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    drive_unit = models.CharField(max_length=20, choices=DRIVE_UNIT_CHOICES)

    class Meta:
        abstract = True


class CarModel(BaseModel, BaseCarCharacteristics):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cars'
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        ordering = ['-updated_at']
