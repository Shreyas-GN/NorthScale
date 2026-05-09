try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

from core.config import settings
from core.logging import logger

def get_supabase_client():
    if not SUPABASE_AVAILABLE:
        logger.warning("Supabase library not installed. Supabase features will be disabled.")
        return None
    try:
        # Check if URL and KEY are provided and look valid
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
            logger.warning("Supabase URL or Key missing in configuration.")
            return None
            
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None

supabase = get_supabase_client()
