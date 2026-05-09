import redis
from app.core.config import settings
from app.core.logging import logger

def get_redis_client():
    try:
        client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_timeout=5
        )
        # Test connection
        client.ping()
        logger.info("Connected to Upstash Redis successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None

# Singleton instance
redis_client = get_redis_client()
