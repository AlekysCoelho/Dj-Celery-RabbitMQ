import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.conf.enable_utc = False
app.conf.update(timezone="America/Sao_Paulo")

app.config_from_object("django.conf:settings", namespace="CELERY")


# CELERY BEAT

app.conf.beat_schedule = {
    "update_tickers_everyday-at-12:00": {
        "task": "stocks.tasks.update_tickers_everyday",
        "schedule": crontab(minute="*/20", hour="8, 10, 12, 14, 16"),
        "options": {"queue": "update_tickers_everyday"},
    },
}


app.autodiscover_tasks()
