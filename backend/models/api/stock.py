"""
models/api/stock.py

API Models for Stocks
"""

from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime

class StockBase(BaseModel):
    ticker: str
    company_name: str
    exchange: str
    sector: Optional[str] = None
    market_cap_category: Optional[str] = None

class StockResponse(StockBase):
    id: str
    is_active: bool
    listed_at: Optional[date] = None

class StockListResponse(BaseModel):
    items: List[StockResponse]
    total: int
    page: int
    limit: int
