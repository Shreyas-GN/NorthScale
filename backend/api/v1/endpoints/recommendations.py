"""
api/v1/endpoints/recommendations.py

Recommendation Endpoints.
Exposes raw deterministic factor breakdowns.
"""

from fastapi import APIRouter, Depends, Path
from datetime import datetime

from supabase import Client
from core.dependencies import get_db
from core.response import SuccessResponse, create_success_response, ResponseMeta
from core.exceptions import AnalysisNotFoundException

router = APIRouter()

@router.get("/{ticker}", response_model=SuccessResponse[dict])
async def get_recommendation_details(
    ticker: str = Path(..., title="Stock Ticker"),
    db: Client = Depends(get_db)
):
    ticker = ticker.upper()
    stock_res = db.table("stocks").select("id").eq("ticker", ticker).execute()
    if not stock_res.data:
        raise AnalysisNotFoundException(ticker)
        
    stock_id = stock_res.data[0]["id"]
    
    rec_res = db.table("recommendations").select("*").eq("stock_id", stock_id).execute()
    if not rec_res.data:
        raise AnalysisNotFoundException(ticker)
        
    rec_data = rec_res.data[0]
    
    # Structure deterministic breakdowns
    result = {
        "ticker": ticker,
        "recommendation": rec_data["recommendation"],
        "conviction_score": float(rec_data["conviction_score"]),
        "confidence_level": rec_data["confidence_level"],
        "composite_score": float(rec_data["composite_score"]),
        "category_scores": {
            "growth": float(rec_data["growth_score"]) if rec_data.get("growth_score") is not None else None,
            "profitability": float(rec_data["profitability_score"]) if rec_data.get("profitability_score") is not None else None,
            "valuation": float(rec_data["valuation_score"]) if rec_data.get("valuation_score") is not None else None,
            "financial_health": float(rec_data["financial_health_score"]) if rec_data.get("financial_health_score") is not None else None,
            "ownership": float(rec_data["ownership_score"]) if rec_data.get("ownership_score") is not None else None,
        },
        "risk_penalty": float(rec_data["risk_score"]) if rec_data.get("risk_score") is not None else 0.0,
        "generated_at": rec_data["generated_at"]
    }
    
    return create_success_response(
        data=result,
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )
