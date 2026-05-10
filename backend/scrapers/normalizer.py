from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Normalization Schemas (Pydantic models for validation)

class NormalizedFinancialSnapshot(BaseModel):
    data_source: str
    fetched_at: datetime
    freshness_score: int = Field(default=100, ge=0, le=100)
    
    # Core mapped fields
    cmp: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    roe: Optional[float] = None
    roce: Optional[float] = None
    debt_to_equity: Optional[float] = None

class NormalizerEngine:
    """
    Validates and normalizes raw dictionary payloads into strictly typed 
    Pydantic models suitable for deterministic Supabase ingestion.
    """
    
    @staticmethod
    def normalize_nse_quote(raw_data: Dict[str, Any]) -> NormalizedFinancialSnapshot:
        """
        Extracts financial metrics from an NSE quote-equity response.
        Example mapping: raw_data['priceInfo']['lastPrice'] -> cmp
        """
        price_info = raw_data.get("priceInfo", {})
        metadata = raw_data.get("metadata", {})
        
        # NSE returns values as numbers or strings, ensure proper extraction
        cmp = price_info.get("lastPrice")
        
        return NormalizedFinancialSnapshot(
            data_source="NSE",
            fetched_at=datetime.utcnow(),
            freshness_score=100,
            cmp=float(cmp) if cmp is not None else None,
            # Further metrics can be mapped here as they become available from other APIs/sections
        )
