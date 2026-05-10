from typing import Dict, Any, Optional
from datetime import datetime
from db.supabase import get_supabase_client
from scrapers.normalizer import NormalizedFinancialSnapshot
from core.logging import logger

class SnapshotBuilder:
    """
    Handles deterministic, append-only insertion of normalized data into Supabase.
    """
    
    def __init__(self):
        self.supabase = get_supabase_client()

    def _ensure_client(self):
        if not self.supabase:
            raise RuntimeError("Supabase client is not initialized.")

    def insert_financial_snapshot(self, stock_id: str, snapshot: NormalizedFinancialSnapshot) -> Optional[Dict[str, Any]]:
        """
        Inserts an immutable financial snapshot.
        """
        self._ensure_client()
        
        payload = {
            "stock_id": stock_id,
            "snapshot_date": snapshot.fetched_at.date().isoformat(),
            "data_source": snapshot.data_source,
            "fetched_at": snapshot.fetched_at.isoformat(),
            "freshness_score": snapshot.freshness_score,
            "cmp": snapshot.cmp,
            "market_cap": snapshot.market_cap,
            "pe_ratio": snapshot.pe_ratio,
            "pb_ratio": snapshot.pb_ratio,
            "roe": snapshot.roe,
            "roce": snapshot.roce,
            "debt_to_equity": snapshot.debt_to_equity
        }

        # Filter out None values to let DB defaults/nulls handle naturally
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            # We use upsert on (stock_id, snapshot_date) as per the UNIQUE INDEX in DB schema
            result = self.supabase.table("stock_financial_snapshots").upsert(payload).execute()
            logger.info(f"Successfully inserted financial snapshot for stock {stock_id}.")
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to insert financial snapshot for stock {stock_id}: {e}")
            return None
