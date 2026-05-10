from celery import Celery
from core.config import settings

celery_app = Celery(
    "northscale",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["jobs.tasks", "jobs.ingestion"]
)

# Queue Configuration
celery_app.conf.task_routes = {
    "jobs.high_priority.*": {"queue": "HIGH"},
    "jobs.medium_priority.*": {"queue": "MEDIUM"},
    "jobs.low_priority.*": {"queue": "LOW"},
}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1, # Better for long running AI/Scraping tasks
)
