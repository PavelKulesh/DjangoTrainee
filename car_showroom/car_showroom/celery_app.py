import os
import time

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_showroom.settings')

app = Celery('car_showroom')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    time.sleep(15)
    print('hello wrld!')


app.conf.beat_schedule = {
    'buy_car_from_provider': {
        'task': 'showroom.tasks.buy_car_from_provider',
        'schedule': crontab(minute='*/10'),
    },
    'profitability_check': {
        'task': 'showroom.tasks.profitability_check',
        'schedule': crontab(minute='*/60'),
    }
}
