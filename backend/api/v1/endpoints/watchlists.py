"""
api/v1/endpoints/watchlists.py

Watchlist endpoints.
"""

from fastapi import APIRouter, Depends, Path, Body
from datetime import datetime
from pydantic import BaseModel

from supabase import Client
from core.dependencies import get_db
from core.response import SuccessResponse, create_success_response, ResponseMeta

router = APIRouter()

class WatchlistCreate(BaseModel):
    name: str
    description: str = ""

@router.get("", response_model=SuccessResponse[dict])
async def get_watchlists(db: Client = Depends(get_db)):
    res = db.table("watchlists").select("*").eq("is_deleted", False).execute()
    return create_success_response(
        data={"watchlists": res.data},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.post("", response_model=SuccessResponse[dict])
async def create_watchlist(data: WatchlistCreate, db: Client = Depends(get_db)):
    # Placeholder
    return create_success_response(
        data={"status": "Watchlist created", "name": data.name},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.get("/{id}", response_model=SuccessResponse[dict])
async def get_watchlist_details(id: str, db: Client = Depends(get_db)):
    # Join stocks and recommendations
    res = db.table("watchlist_stocks").select("*, stocks(*, recommendations(recommendation, conviction_score))").eq("watchlist_id", id).execute()
    return create_success_response(
        data={"id": id, "stocks": res.data},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.post("/{id}/stocks/{stock_id}", response_model=SuccessResponse[dict])
async def add_stock(id: str, stock_id: str, db: Client = Depends(get_db)):
    # Placeholder
    return create_success_response(
        data={"status": "Stock added"},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.delete("/{id}/stocks/{stock_id}", response_model=SuccessResponse[dict])
async def remove_stock(id: str, stock_id: str, db: Client = Depends(get_db)):
    # Placeholder
    return create_success_response(
        data={"status": "Stock removed"},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )
