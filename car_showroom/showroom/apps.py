from django.apps import AppConfig


class ShowroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'showroom'

    def ready(self):
        from . import signals
        from .models import ShowroomCarCharacteristics
        signals.post_save.connect(signals.added_showroom, sender=ShowroomCarCharacteristics)
