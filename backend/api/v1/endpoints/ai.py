"""
api/v1/endpoints/ai.py

AI Endpoints.
Serves raw AI generation data, query interface, and command parsing.
"""

from fastapi import APIRouter, Depends, Path, Body
from datetime import datetime
from pydantic import BaseModel

from supabase import Client
from core.dependencies import get_db
from core.response import SuccessResponse, create_success_response, ResponseMeta
from core.exceptions import NotFoundException

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class CommandRequest(BaseModel):
    command: str

@router.get("/thesis/{ticker}", response_model=SuccessResponse[dict])
async def get_ai_thesis(
    ticker: str = Path(..., title="Stock Ticker"),
    db: Client = Depends(get_db)
):
    ticker = ticker.upper()
    stock_res = db.table("stocks").select("id").eq("ticker", ticker).execute()
    if not stock_res.data:
        raise NotFoundException(f"Stock {ticker} not found")
        
    stock_id = stock_res.data[0]["id"]
    
    thesis_res = db.table("ai_theses").select("*").eq("stock_id", stock_id).order("generated_at", desc=True).limit(1).execute()
    if not thesis_res.data:
        raise NotFoundException(f"No AI thesis generated for {ticker}")
        
    thesis_data = thesis_res.data[0]
    
    return create_success_response(
        data=thesis_data,
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.post("/query", response_model=SuccessResponse[dict])
async def query_ai(request: QueryRequest):
    # MVP: placeholder for contextual stock research query
    # In full implementation, this routes to GroqClient
    return create_success_response(
        data={"response": f"AI query received: {request.query}. (MVP Placeholder)"},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )

@router.post("/commands", response_model=SuccessResponse[dict])
async def command_ai(request: CommandRequest):
    # MVP: placeholder for command parsing routing
    return create_success_response(
        data={"action_parsed": "none", "original_command": request.command},
        meta=ResponseMeta(generated_at=datetime.utcnow().isoformat())
    )
