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
    BRAND_CHOICES = [
        ('Toyota', 'Toyota'),
        ('Honda', 'Honda'),
        ('Ford', 'Ford'),
        ('BMW', 'BMW'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Audi', 'Audi'),
        ('Chevrolet', 'Chevrolet'),
        ('Volkswagen', 'Volkswagen'),
        ('Hyundai', 'Hyundai'),
        ('Nissan', 'Nissan'),
        ('Kia', 'Kia'),
        ('Volvo', 'Volvo'),
        ('Subaru', 'Subaru'),
        ('Mazda', 'Mazda'),
        ('Lexus', 'Lexus'),
        ('Tesla', 'Tesla'),
        ('Porsche', 'Porsche'),
        ('Jeep', 'Jeep'),
        ('Land Rover', 'Land Rover'),
        ('Ferrari', 'Ferrari'),
        ('Lamborghini', 'Lamborghini'),
        ('Maserati', 'Maserati'),
        ('Bentley', 'Bentley'),
    ]

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

    brand = models.CharField(max_length=20, choices=BRAND_CHOICES)
    issue_year = models.PositiveSmallIntegerField(default=2010)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES)
    engine_capacity = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0)], default=0)
    engine_power = models.PositiveIntegerField(default=0)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    drive_unit = models.CharField(max_length=20, choices=DRIVE_UNIT_CHOICES)

    class Meta:
        abstract = True
