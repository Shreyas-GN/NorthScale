"""
core/response.py

Standardized API response and error envelopes for NorthScale REST API.
"""

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")

class ResponseMeta(BaseModel):
    cached: bool = False
    generated_at: str
    data_freshness: Optional[int] = None

class SuccessResponse(BaseModel, Generic[DataT]):
    success: bool = True
    data: DataT
    meta: ResponseMeta

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail

def create_success_response(data: Any, meta: ResponseMeta) -> SuccessResponse:
    return SuccessResponse(data=data, meta=meta)

def create_error_response(code: str, message: str) -> ErrorResponse:
    return ErrorResponse(error=ErrorDetail(code=code, message=message))
