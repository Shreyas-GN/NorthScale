from supabase import create_client, Client
from core.config import settings
from core.logging import logger

supabase: Client | None = None


def get_supabase_client() -> Client | None:
    global supabase

    if supabase:
        return supabase

    try:
        supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY,
        )

        logger.info("Successfully connected to Supabase")

        return supabase

    except Exception as e:
        logger.exception(f"Failed to initialize Supabase client: {e}")
        return None
