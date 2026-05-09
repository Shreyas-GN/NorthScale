import redis
from core.config import settings
from core.logging import logger

def get_redis_connection():
    try:
        pool = redis.ConnectionPool.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_timeout=5,
            retry_on_timeout=True
        )
        r = redis.Redis(connection_pool=pool)
        # Test connection
        r.ping()
        logger.info("Successfully connected to Redis")
        return r
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        # We don't necessarily want to crash if Redis is down, 
        # but for Phase 1 we should log it clearly.
        return None

redis_client = get_redis_connection()
