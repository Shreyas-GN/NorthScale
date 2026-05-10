"""
api/v1/endpoints/insights.py

Insights and Alerts endpoints.
Chronological contextual feeds.
"""

from fastapi import APIRouter, Depends, Query
from datetime import datetime

from supabase import Client
from core.dependencies import get_db
from core.response import SuccessResponse, create_success_response, ResponseMeta

router = APIRouter()

@router.get("", response_model=SuccessResponse[dict])
async def get_insights(
    limit: int = Query(20, ge=1, le=50),
    db: Client = Depends(get_db)
):
    res = db.table("ai_insights").select("*, stocks(ticker, company_name)").order("generated_at", desc=True).limit(limit).execute()
    
    return create_success_response(
        data={"insights": res.data},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.get("/alerts", response_model=SuccessResponse[dict])
async def get_alerts(
    limit: int = Query(20, ge=1, le=50),
    db: Client = Depends(get_db)
):
    res = db.table("alerts").select("*, stocks(ticker)").order("triggered_at", desc=True).limit(limit).execute()
    
    return create_success_response(
        data={"alerts": res.data},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )
