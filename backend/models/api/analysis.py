"""
models/api/analysis.py

API Models for Analysis (Unified response)
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class AnalysisResponse(BaseModel):
    ticker: str
    company_name: str
    sector: str
    recommendation: str
    conviction_score: float
    confidence_level: str
    
    # AI Thesis
    thesis_summary: Optional[str] = None
    bullish_factors: List[str] = []
    bearish_factors: List[str] = []
    valuation_summary: Optional[str] = None
    overall_view: Optional[str] = None
    
    # Deterministic signals
    positive_signals: List[str] = []
    negative_signals: List[str] = []
    sector_context: Optional[str] = None
    confidence_reasoning: Optional[str] = None
    
    # Risk
    risk_score: float
    risk_summary: Optional[str] = None
    
    # Metadata
    freshness_score: int
    data_source: str
    snapshot_date: str
    is_fallback: bool = False
