from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ShowroomCarCharacteristics
from .tasks import get_showroom_cars


@receiver(post_save, sender=ShowroomCarCharacteristics)
def added_showroom(sender, created, instance, **kwargs):
    if created:
        get_showroom_cars.delay(instance.id)
