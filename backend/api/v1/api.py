from fastapi import APIRouter

from api.v1.endpoints import health, stocks, analysis, recommendations, ai, portfolio, search, insights, watchlists

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
api_router.include_router(watchlists.router, prefix="/watchlists", tags=["watchlists"])
