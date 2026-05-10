"""
core/cache.py

Redis caching layer for API.
Supports endpoint-level caching with graceful failure degradation if Redis is unavailable.
"""

import json
from typing import Any, Optional
import redis.asyncio as redis
from core.config import settings
from core.logging import logger

redis_client: Optional[redis.Redis] = None

async def get_redis() -> Optional[redis.Redis]:
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            # Test connection
            await redis_client.ping()
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Running without cache.")
            redis_client = None
    return redis_client

async def get_cache(key: str) -> Optional[Any]:
    client = await get_redis()
    if not client:
        return None
    try:
        data = await client.get(key)
        return json.loads(data) if data else None
    except Exception as e:
        logger.warning(f"Redis get failed for {key}: {e}")
        return None

async def set_cache(key: str, value: Any, ttl_seconds: int = 900) -> bool:
    client = await get_redis()
    if not client:
        return False
    try:
        await client.setex(key, ttl_seconds, json.dumps(value))
        return True
    except Exception as e:
        logger.warning(f"Redis set failed for {key}: {e}")
        return False

async def invalidate_cache(key: str) -> bool:
    client = await get_redis()
    if not client:
        return False
    try:
        await client.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Redis invalidate failed for {key}: {e}")
        return False

async def invalidate_pattern(pattern: str) -> bool:
    """Invalidate all keys matching a pattern (e.g., analysis:*)"""
    client = await get_redis()
    if not client:
        return False
    try:
        keys = await client.keys(pattern)
        if keys:
            await client.delete(*keys)
        return True
    except Exception as e:
        logger.warning(f"Redis pattern invalidate failed for {pattern}: {e}")
        return False

class CacheKey:
    @staticmethod
    def analysis(ticker: str) -> str:
        return f"analysis:{ticker.upper()}"
        
    @staticmethod
    def thesis(ticker: str) -> str:
        return f"thesis:{ticker.upper()}"
        
    @staticmethod
    def portfolio(portfolio_id: str) -> str:
        return f"portfolio:{portfolio_id}"
        
    @staticmethod
    def recommendations(ticker: str) -> str:
        return f"recommendations:{ticker.upper()}"
        
    @staticmethod
    def stock(ticker: str) -> str:
        return f"stock:{ticker.upper()}"

class CacheTTL:
    ANALYSIS = 900       # 15 minutes
    THESIS = 1800        # 30 minutes
    PORTFOLIO = 300      # 5 minutes
    STOCK_META = 3600    # 1 hour
