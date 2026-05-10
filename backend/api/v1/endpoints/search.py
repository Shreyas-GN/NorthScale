"""
api/v1/endpoints/search.py

Fast search endpoint for tickers and companies.
"""

from fastapi import APIRouter, Depends, Query
from datetime import datetime

from supabase import Client
from core.dependencies import get_db
from core.response import SuccessResponse, create_success_response, ResponseMeta

router = APIRouter()

@router.get("", response_model=SuccessResponse[dict])
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    db: Client = Depends(get_db)
):
    query = f"%{q}%"
    
    # Prioritize ticker exact match, then ticker like, then company name like
    # Supabase / PostgREST doesn't support complex weighting natively in a simple query,
    # so we'll fetch matches and sort them in Python since the dataset size for search result is small.
    
    res = db.table("stocks").select("id, ticker, company_name, exchange, sectors(slug)").or_(f"ticker.ilike.{query},company_name.ilike.{query}").limit(20).execute()
    
    results = res.data
    
    # Sort: Exact ticker match > Ticker starts with > Company name
    q_upper = q.upper()
    
    def sort_key(item):
        ticker = item["ticker"].upper()
        if ticker == q_upper:
            return 0
        if ticker.startswith(q_upper):
            return 1
        return 2
        
    results.sort(key=sort_key)
    
    return create_success_response(
        data={"results": results},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )
