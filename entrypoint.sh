#!/bin/sh

case "$1" in
  "django")
    python manage.py runserver 0.0.0.0:8000
    ;;
  "celery")
    celery -A car_showroom worker --loglevel=info
    ;;
  "celery_beat")
    celery -A car_showroom beat
    ;;
  "flower")
    celery -A car_showroom flower
    ;;
  *)
    echo "Unknown service: $1"
    ;;
esac