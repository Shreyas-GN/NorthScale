from fastapi import APIRouter
from db.redis import redis_client
from db.supabase import get_supabase_client
from core.logging import logger

router = APIRouter()

@router.get("/health")
async def health_check():
    client = get_supabase_client()
    health_status = {
        "status": "ok",
        "services": {
            "redis": "connected" if redis_client and redis_client.ping() else "disconnected",
            "supabase": "connected" if client else "unavailable"
        }
    }
    logger.debug(f"Health check performed: {health_status}")
    return health_status
