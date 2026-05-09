from core.celery_app import celery_app
from core.logging import logger

@celery_app.task(name="jobs.tasks.health_check")
def health_check_task():
    logger.info("Celery health check task running")
    return {"status": "ok"}
