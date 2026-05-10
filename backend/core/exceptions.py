"""
core/exceptions.py

Centralized exception handling for the FastAPI layer.
Translates Python exceptions into structured API ErrorResponses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from core.response import create_error_response
from core.logging import logger

class NorthScaleException(Exception):
    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.status_code = status_code

class NotFoundException(NorthScaleException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            code="NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class AnalysisNotFoundException(NorthScaleException):
    def __init__(self, ticker: str):
        super().__init__(
            code="ANALYSIS_NOT_FOUND",
            message=f"Analysis not found for {ticker}",
            status_code=status.HTTP_404_NOT_FOUND
        )

async def northscale_exception_handler(request: Request, exc: NorthScaleException):
    logger.warning(f"Handled API Exception: {exc.code} - {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(exc.code, exc.message).model_dump()
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response("INTERNAL_ERROR", "An unexpected error occurred").model_dump()
    )

def setup_exception_handlers(app):
    app.add_exception_handler(NorthScaleException, northscale_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
