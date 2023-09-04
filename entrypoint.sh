#!/bin/sh

case "$1" in
  "django")
    gunicorn car_showroom.wsgi:application -c gunicorn_config.py
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