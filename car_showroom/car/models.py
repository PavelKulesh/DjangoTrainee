from django.db import models
from car_showroom.models import BaseModel, BaseCarCharacteristics


class CarModel(BaseModel, BaseCarCharacteristics):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.brand} {self.name}'

    class Meta:
        db_table = 'cars'
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        ordering = ['-updated_at']
