"""
api/v1/endpoints/portfolio.py

Portfolio endpoints.
"""

from fastapi import APIRouter, Depends, Path
from datetime import datetime

from supabase import Client
from core.dependencies import get_db
from core.response import SuccessResponse, create_success_response, ResponseMeta

router = APIRouter()

@router.get("", response_model=SuccessResponse[dict])
async def get_portfolio(db: Client = Depends(get_db)):
    # MVP: Fetch default portfolio
    # Since auth is deferred, we just fetch the first portfolio or create a dummy structure
    port_res = db.table("portfolios").select("*").limit(1).execute()
    if not port_res.data:
        return create_success_response(
            data={"holdings": [], "summary": "No portfolio found"},
            meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
        )
        
    portfolio_id = port_res.data[0]["id"]
    
    holdings_res = db.table("portfolio_holdings").select("*, stocks(ticker, company_name)").eq("portfolio_id", portfolio_id).eq("is_deleted", False).execute()
    
    return create_success_response(
        data={"id": portfolio_id, "holdings": holdings_res.data},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.post("/holdings", response_model=SuccessResponse[dict])
async def add_holding(db: Client = Depends(get_db)):
    # Placeholder for adding holding
    return create_success_response(
        data={"status": "Holding added placeholder"},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.delete("/holdings/{id}", response_model=SuccessResponse[dict])
async def remove_holding(id: str, db: Client = Depends(get_db)):
    # Placeholder for removing holding
    return create_success_response(
        data={"status": f"Holding {id} removed placeholder"},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.get("/intelligence", response_model=SuccessResponse[dict])
async def get_portfolio_intelligence(db: Client = Depends(get_db)):
    # Placeholder for fetching latest portfolio_snapshots with AI summary
    return create_success_response(
        data={"ai_summary": "Placeholder intelligence based on deterministic data."},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )
