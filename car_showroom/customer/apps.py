from django.apps import AppConfig


class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer'

    def ready(self):
        from . import signals
        from .models import CustomerOffer
        signals.post_save.connect(signals.added_showroom, sender=CustomerOffer)
