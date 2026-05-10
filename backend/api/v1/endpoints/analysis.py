"""
api/v1/endpoints/analysis.py

Core Analysis Endpoints.
Serves the unified deterministic truth and AI thesis for the frontend.
"""

from fastapi import APIRouter, Depends, Path
from datetime import datetime

from supabase import Client
from core.dependencies import get_db
from core.response import SuccessResponse, create_success_response, ResponseMeta
from core.exceptions import AnalysisNotFoundException
from models.api.analysis import AnalysisResponse
from core.cache import get_cache, set_cache, CacheKey, CacheTTL
from core.logging import logger

router = APIRouter()

@router.get("/{ticker}", response_model=SuccessResponse[AnalysisResponse])
async def get_analysis(
    ticker: str = Path(..., title="Stock Ticker"),
    db: Client = Depends(get_db)
):
    ticker = ticker.upper()
    cache_key = CacheKey.analysis(ticker)
    
    # 2. Check Redis cache
    cached_data = await get_cache(cache_key)
    if cached_data:
        return create_success_response(
            data=cached_data,
            meta=ResponseMeta(cached=True, generated_at=datetime.utcnow().isoformat())
        )
        
    # 1. Validate ticker & Fetch stock
    stock_res = db.table("stocks").select("id, company_name, sectors(slug)").eq("ticker", ticker).execute()
    if not stock_res.data:
        raise AnalysisNotFoundException(ticker)
        
    stock_id = stock_res.data[0]["id"]
    company_name = stock_res.data[0]["company_name"]
    sector = stock_res.data[0].get("sectors", {}).get("slug", "unknown")
    
    # 3. Fetch latest financial snapshot (for freshness)
    fin_res = db.table("stock_financial_snapshots").select("snapshot_date, data_source, freshness_score").eq("stock_id", stock_id).order("snapshot_date", desc=True).limit(1).execute()
    if not fin_res.data:
        raise AnalysisNotFoundException(ticker)
        
    fin_data = fin_res.data[0]
    
    # 4. Fetch latest recommendation
    rec_res = db.table("recommendations").select("*").eq("stock_id", stock_id).execute()
    if not rec_res.data:
        raise AnalysisNotFoundException(ticker)
        
    rec_data = rec_res.data[0]
    
    # 5. Fetch latest AI thesis
    # Join ai_theses with recommendation_id to ensure we get the thesis tied to the active recommendation
    thesis_res = db.table("ai_theses").select("*").eq("stock_id", stock_id).order("generated_at", desc=True).limit(1).execute()
    thesis_data = thesis_res.data[0] if thesis_res.data else {}

    # Extract deterministic explainability (simulated extraction from recommendation row for MVP if not fully expanded in DB)
    # The MVP DB schema stores category scores and risk score. We might need to reconstruct signals if they aren't stored as arrays.
    # Wait, the DB schema for recommendations didn't have positive_signals arrays. 
    # For a true unified response, we rely on the thesis_data which has key_strengths / key_risks derived from it.
    
    analysis = AnalysisResponse(
        ticker=ticker,
        company_name=company_name,
        sector=sector,
        recommendation=rec_data["recommendation"],
        conviction_score=float(rec_data["conviction_score"]),
        confidence_level=rec_data["confidence_level"],
        
        thesis_summary=thesis_data.get("thesis_summary"),
        bullish_factors=thesis_data.get("key_strengths", []),
        bearish_factors=thesis_data.get("key_risks", []),
        valuation_summary=thesis_data.get("valuation_perspective"),
        overall_view=thesis_data.get("overall_view"),
        
        positive_signals=thesis_data.get("key_strengths", []), # Fallback mapping if signals not in rec table
        negative_signals=thesis_data.get("key_risks", []),
        
        risk_score=float(rec_data["risk_score"]) if rec_data.get("risk_score") is not None else 0.0,
        risk_summary=thesis_data.get("confidence_note"),
        
        freshness_score=fin_data.get("freshness_score", 100),
        data_source=fin_data.get("data_source", "System"),
        snapshot_date=fin_data.get("snapshot_date", ""),
        is_fallback=thesis_data.get("is_fallback", False)
    )
    
    # Cache result
    await set_cache(cache_key, analysis.model_dump(), CacheTTL.ANALYSIS)
    
    return create_success_response(
        data=analysis,
        meta=ResponseMeta(
            cached=False, 
            generated_at=datetime.utcnow().isoformat(),
            data_freshness=fin_data.get("freshness_score", 100)
        )
    )

@router.get("/{ticker}/history", response_model=SuccessResponse[dict])
async def get_analysis_history(
    ticker: str = Path(..., title="Stock Ticker"),
    db: Client = Depends(get_db)
):
    ticker = ticker.upper()
    stock_res = db.table("stocks").select("id").eq("ticker", ticker).execute()
    if not stock_res.data:
        raise AnalysisNotFoundException(ticker)
        
    stock_id = stock_res.data[0]["id"]
    
    history_res = db.table("recommendation_history").select("*").eq("stock_id", stock_id).order("generated_at", desc=True).execute()
    
    return create_success_response(
        data={"history": history_res.data},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )
