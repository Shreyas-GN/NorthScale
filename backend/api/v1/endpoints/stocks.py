"""
api/v1/endpoints/stocks.py

Stock endpoints.
"""

from fastapi import APIRouter, Depends, Query, Path
from typing import Optional
from datetime import datetime
import json

from supabase import Client
from core.dependencies import get_db
from core.response import SuccessResponse, create_success_response, ResponseMeta
from core.exceptions import NotFoundException
from models.api.stock import StockListResponse, StockResponse
from core.cache import get_cache, set_cache, CacheKey, CacheTTL

router = APIRouter()

@router.get("", response_model=SuccessResponse[StockListResponse])
async def list_stocks(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    sector: Optional[str] = None,
    recommendation: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("market_cap", regex="^(market_cap|company_name|ticker)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Client = Depends(get_db)
):
    # This endpoint is dynamic, caching might be complex with all filters,
    # but we can cache standard queries if needed. For MVP, query DB directly.
    
    query = db.table("stocks").select("*, sectors(slug)", count="exact")
    
    if search:
        query = query.ilike("ticker", f"%{search}%")
        
    if sector:
        # Note: assumes frontend passes sector slug. We might need to join or assume sector_id if simplified.
        # Supabase allows inner joins via foreign tables.
        query = query.eq("sectors.slug", sector)
        
    if sort_by == "ticker":
        query = query.order("ticker", desc=(sort_order == "desc"))
    elif sort_by == "company_name":
        query = query.order("company_name", desc=(sort_order == "desc"))
        
    # Recommendation filtering requires joining the active recommendations table.
    # If recommendation filter is active, we should query recommendations table instead and join stocks.
    # For MVP simplicity, we apply pagination to the stock table.
    
    offset = (page - 1) * limit
    query = query.range(offset, offset + limit - 1)
    
    res = query.execute()
    
    items = []
    for row in res.data:
        items.append(StockResponse(
            id=row["id"],
            ticker=row["ticker"],
            company_name=row["company_name"],
            exchange=row["exchange"],
            sector=row.get("sectors", {}).get("slug") if row.get("sectors") else None,
            market_cap_category=row.get("market_cap_category"),
            is_active=row["is_active"],
            listed_at=row.get("listed_at")
        ))
        
    data = StockListResponse(
        items=items,
        total=res.count if res.count else 0,
        page=page,
        limit=limit
    )
    
    return create_success_response(
        data=data,
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.get("/{ticker}", response_model=SuccessResponse[dict])
async def get_stock(
    ticker: str = Path(..., title="Stock Ticker"),
    db: Client = Depends(get_db)
):
    cache_key = CacheKey.stock(ticker)
    cached_data = await get_cache(cache_key)
    
    if cached_data:
        return create_success_response(
            data=cached_data,
            meta=ResponseMeta(cached=True, generated_at=datetime.utcnow().isoformat())
        )
        
    # Fetch stock
    stock_res = db.table("stocks").select("*, sectors(slug)").eq("ticker", ticker.upper()).execute()
    if not stock_res.data:
        raise NotFoundException(f"Stock {ticker} not found")
        
    stock_data = stock_res.data[0]
    
    # Fetch active recommendation summary
    rec_res = db.table("recommendations").select("recommendation, conviction_score, confidence_level").eq("stock_id", stock_data["id"]).execute()
    rec_summary = rec_res.data[0] if rec_res.data else None
    
    result = {
        "stock": {
            "id": stock_data["id"],
            "ticker": stock_data["ticker"],
            "company_name": stock_data["company_name"],
            "exchange": stock_data["exchange"],
            "sector": stock_data.get("sectors", {}).get("slug") if stock_data.get("sectors") else None,
            "market_cap_category": stock_data.get("market_cap_category")
        },
        "recommendation_summary": rec_summary
    }
    
    await set_cache(cache_key, result, CacheTTL.STOCK_META)
    
    return create_success_response(
        data=result,
        meta=ResponseMeta(cached=False, generated_at=datetime.utcnow().isoformat())
    )
