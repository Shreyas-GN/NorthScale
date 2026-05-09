from supabase import create_client, Client
from app.core.config import settings
from app.core.logging import logger

def get_supabase_client() -> Client:
    try:
        client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        raise e

# Singleton instance
supabase_client = get_supabase_client()
