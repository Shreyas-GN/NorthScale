import time
from typing import Optional
from core.celery_app import celery_app
from core.logging import logger
from scrapers.nse import NSEScraper
from scrapers.normalizer import NormalizerEngine
from services.snapshot import SnapshotBuilder
from services.scraping_logs import ScrapingLogger

@celery_app.task(name="jobs.ingestion.scrape_nse_equity", bind=True, max_retries=3)
def scrape_nse_equity(self, job_id: str, stock_id: str, ticker: str):
    """
    Celery task to scrape equity data from NSE, normalize it, and snapshot it.
    """
    logger.info(f"Starting NSE ingestion for {ticker} (Job: {job_id})")
    
    scraper = NSEScraper()
    snapshot_builder = SnapshotBuilder()
    scraper_logger = ScrapingLogger()
    
    start_time = time.time()
    
    try:
        # 1. Update Job Status to RUNNING
        scraper_logger.update_job_status(job_id, "RUNNING")
        
        # 2. Fetch Raw Data
        raw_data = scraper.fetch_data(ticker)
        if not raw_data:
            raise ValueError(f"No data returned from NSE for {ticker}")
            
        # 3. Normalize Data
        normalized_data = NormalizerEngine.normalize_nse_quote(raw_data)
        
        # 4. Insert Snapshot
        inserted = snapshot_builder.insert_financial_snapshot(stock_id, normalized_data)
        if not inserted:
            raise ValueError(f"Failed to persist snapshot for {ticker}")
            
        # 5. Log Success
        latency_ms = int((time.time() - start_time) * 1000)
        scraper_logger.log_attempt(
            job_id=job_id,
            stock_id=stock_id,
            source="NSE",
            status="SUCCESS",
            records_saved=1,
            latency_ms=latency_ms
        )
        scraper_logger.update_job_status(job_id, "SUCCESS")
        
        return {"status": "success", "ticker": ticker, "latency_ms": latency_ms}
        
    except Exception as exc:
        latency_ms = int((time.time() - start_time) * 1000)
        error_msg = str(exc)
        logger.error(f"Ingestion failed for {ticker}: {error_msg}")
        
        scraper_logger.log_attempt(
            job_id=job_id,
            stock_id=stock_id,
            source="NSE",
            status="FAILED",
            records_saved=0,
            latency_ms=latency_ms,
            error_message=error_msg
        )
        scraper_logger.update_job_status(job_id, "FAILED", error_message=error_msg)
        
        # Exponential backoff retry
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
