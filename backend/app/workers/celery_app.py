from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "polymarket_engine",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.task_routes = {
    "app.workers.tasks.*": {"queue": "engine"},
}
celery_app.conf.beat_schedule = {
    "refresh-simplified-markets-every-15m": {
        "task": "app.workers.tasks.refresh_market_data",
        "schedule": crontab(minute="*/15"),
        "args": (1,),
    },
    "refresh-order-books-every-5m": {
        "task": "app.workers.tasks.refresh_order_books",
        "schedule": crontab(minute="*/5"),
        "args": (50,),
    },
}
celery_app.conf.timezone = "Europe/Berlin"
