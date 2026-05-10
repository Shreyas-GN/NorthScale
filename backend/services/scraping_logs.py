from typing import Optional, Dict, Any
from db.supabase import get_supabase_client
from core.logging import logger

class ScrapingLogger:
    """
    Handles logging of scraping events, successes, and failures into the 
    `scraping_logs` and `scraping_jobs` database tables.
    """
    
    def __init__(self):
        self.supabase = get_supabase_client()

    def _ensure_client(self):
        if not self.supabase:
            raise RuntimeError("Supabase client is not initialized.")

    def log_attempt(self, job_id: str, stock_id: Optional[str], source: str, status: str, 
                    records_saved: int = 0, latency_ms: Optional[int] = None, error_message: Optional[str] = None) -> None:
        """
        Logs a specific scraping attempt to the scraping_logs table.
        Status must be one of: 'SUCCESS', 'FAILED', 'PARTIAL', 'BLOCKED'.
        """
        self._ensure_client()
        
        payload = {
            "job_id": job_id,
            "stock_id": stock_id,
            "source": source,
            "status": status,
            "records_saved": records_saved,
            "latency_ms": latency_ms,
            "error_message": error_message
        }
        
        # Filter None
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            self.supabase.table("scraping_logs").insert(payload).execute()
        except Exception as e:
            # We use core logger if DB logging fails to avoid recursive failure
            logger.error(f"Failed to write to scraping_logs table: {e}")

    def update_job_status(self, job_id: str, status: str, error_message: Optional[str] = None) -> None:
        """
        Updates the parent job status in scraping_jobs.
        Status must be one of: 'PENDING', 'RUNNING', 'SUCCESS', 'FAILED', 'RETRYING', 'CANCELLED'.
        """
        self._ensure_client()
        
        payload = {"status": status}
        if error_message:
            payload["error_message"] = error_message
            
        try:
            self.supabase.table("scraping_jobs").update(payload).eq("id", job_id).execute()
        except Exception as e:
            logger.error(f"Failed to update scraping_jobs table for job {job_id}: {e}")
