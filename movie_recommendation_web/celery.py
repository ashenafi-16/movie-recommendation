import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_recommendation_web.settings")

app = Celery("movie_recommendation_web")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app.conf.result_backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app.autodiscover_tasks()
