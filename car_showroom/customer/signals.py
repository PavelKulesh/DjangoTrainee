from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerOffer
from .tasks import buy_offered_car


@receiver(post_save, sender=CustomerOffer)
def added_showroom(sender, created, instance, **kwargs):
    if created:
        buy_offered_car.delay(instance.id)
