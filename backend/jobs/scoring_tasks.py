"""
jobs/scoring_tasks.py

Celery tasks for the Phase 3 deterministic scoring pipeline.

Tasks:
  - score_stock_task: Run the full intelligence pipeline for a single stock
  - score_all_stocks_task: Fan out scoring across all active stocks
  - score_sector_task: Score all stocks in a specific sector

All tasks are:
  - deterministic
  - idempotent (safe to re-run)
  - auditable (full logging)
  - retried on failure
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

from celery import group

from core.celery_app import celery_app
from core.logging import logger
from db.supabase import get_supabase_client
from engines.models import FinancialMetricsInput
from engines.pipeline import run_scoring_pipeline
from services.recommendation_service import RecommendationService


@celery_app.task(
    name="jobs.scoring_tasks.score_stock_task",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def score_stock_task(self, stock_id: str, ticker: str, sector_slug: str) -> Dict[str, Any]:
    """
    Run the full deterministic scoring pipeline for a single stock.

    Fetches the latest financial and ownership snapshot from Supabase,
    constructs FinancialMetricsInput, runs pipeline, and persists result.

    Returns a summary dict for logging/monitoring.
    """
    logger.info(f"[SCORE_TASK] Starting scoring pipeline for {ticker} ({stock_id})")

    supabase = get_supabase_client()
    if not supabase:
        logger.error(f"[SCORE_TASK] Supabase unavailable — cannot score {ticker}")
        raise self.retry(exc=RuntimeError("Supabase unavailable"))

    # --- Fetch latest financial snapshot ---
    try:
        fin_res = (
            supabase.table("stock_financial_snapshots")
            .select("*")
            .eq("stock_id", stock_id)
            .order("snapshot_date", desc=True)
            .limit(1)
            .execute()
        )
        fin_data: Optional[Dict] = fin_res.data[0] if fin_res.data else None
    except Exception as e:
        logger.error(f"[SCORE_TASK] Failed to fetch financial snapshot for {ticker}: {e}")
        raise self.retry(exc=e)

    if not fin_data:
        logger.warning(f"[SCORE_TASK] No financial snapshot found for {ticker} — skipping")
        return {"ticker": ticker, "status": "skipped", "reason": "no_financial_snapshot"}

    # --- Fetch latest ownership snapshot ---
    try:
        own_res = (
            supabase.table("stock_ownership_snapshots")
            .select("*")
            .eq("stock_id", stock_id)
            .order("quarter_end_date", desc=True)
            .limit(1)
            .execute()
        )
        own_data: Optional[Dict] = own_res.data[0] if own_res.data else None
    except Exception as e:
        logger.warning(f"[SCORE_TASK] Failed to fetch ownership snapshot for {ticker}: {e}")
        own_data = None

    # --- Build FinancialMetricsInput ---
    try:
        metrics = FinancialMetricsInput(
            stock_id=stock_id,
            ticker=ticker,
            sector_slug=sector_slug,
            snapshot_date=date.fromisoformat(fin_data["snapshot_date"]),
            financial_snapshot_id=fin_data.get("id"),
            ownership_snapshot_id=own_data.get("id") if own_data else None,

            # Profitability
            roe=fin_data.get("roe"),
            roce=fin_data.get("roce"),
            net_profit_margin=fin_data.get("net_profit_margin"),
            operating_margin=fin_data.get("operating_margin"),
            gross_margin=fin_data.get("gross_margin"),
            ebitda_margin=fin_data.get("ebitda_margin"),

            # Growth
            revenue_1y_growth=fin_data.get("revenue_1y_growth"),
            revenue_3y_cagr=fin_data.get("revenue_3y_cagr"),
            revenue_5y_cagr=fin_data.get("revenue_5y_cagr"),
            profit_1y_growth=fin_data.get("profit_1y_growth"),
            profit_3y_cagr=fin_data.get("profit_3y_cagr"),
            profit_5y_cagr=fin_data.get("profit_5y_cagr"),

            # Financial Health
            debt_to_equity=fin_data.get("debt_to_equity"),
            current_ratio=fin_data.get("current_ratio"),
            interest_coverage=fin_data.get("interest_coverage"),
            free_cash_flow=fin_data.get("free_cash_flow"),
            cash_and_equivalents=fin_data.get("cash_and_equivalents"),
            net_profit_ttm=fin_data.get("net_profit_ttm"),

            # Valuation
            pe_ratio=fin_data.get("pe_ratio"),
            pb_ratio=fin_data.get("pb_ratio"),
            ev_to_ebitda=fin_data.get("ev_to_ebitda"),
            price_to_sales=fin_data.get("price_to_sales"),
            cmp=fin_data.get("cmp"),
            market_cap=fin_data.get("market_cap"),

            # Ownership (from ownership snapshot)
            promoter_holding=own_data.get("promoter_holding") if own_data else None,
            promoter_pledge_pct=own_data.get("promoter_pledge_pct") if own_data else None,
            fii_holding=own_data.get("fii_holding") if own_data else None,
            dii_holding=own_data.get("dii_holding") if own_data else None,
            promoter_change_qoq=own_data.get("promoter_change_qoq") if own_data else None,
            fii_change_qoq=own_data.get("fii_change_qoq") if own_data else None,
            dii_change_qoq=own_data.get("dii_change_qoq") if own_data else None,

            # Banking-specific
            casa_ratio=fin_data.get("casa_ratio"),
            gnpa_ratio=fin_data.get("gnpa_ratio"),
            nnpa_ratio=fin_data.get("nnpa_ratio"),
            nim=fin_data.get("nim"),
            car_ratio=fin_data.get("car_ratio"),

            # Data quality
            freshness_score=fin_data.get("freshness_score", 100),
            data_source=fin_data.get("data_source", "UNKNOWN"),
        )
    except Exception as e:
        logger.error(f"[SCORE_TASK] Failed to construct FinancialMetricsInput for {ticker}: {e}")
        return {"ticker": ticker, "status": "error", "reason": str(e)}

    # --- Run pipeline ---
    try:
        result = run_scoring_pipeline(metrics)
    except Exception as e:
        logger.error(f"[SCORE_TASK] Pipeline failed for {ticker}: {e}")
        raise self.retry(exc=e)

    # --- Persist result ---
    try:
        service = RecommendationService()
        persisted = service.persist_scoring_result(result)
    except Exception as e:
        logger.error(f"[SCORE_TASK] Failed to persist result for {ticker}: {e}")
        raise self.retry(exc=e)

    return {
        "ticker": ticker,
        "status": "success",
        "recommendation": result.recommendation.value,
        "conviction_score": float(result.conviction.conviction_score),
        "conviction_tier": result.conviction.conviction_tier.value,
        "confidence_level": result.conviction.confidence_level.value,
        "composite_score": float(result.composite_score),
        "risk_penalty": float(result.explainability.risk_output.total_risk_penalty),
        "persisted": persisted,
    }


@celery_app.task(name="jobs.scoring_tasks.score_all_stocks_task", bind=True)
def score_all_stocks_task(self) -> Dict[str, Any]:
    """
    Fan out the scoring pipeline across all active stocks.
    Fetches stock list from Supabase and dispatches individual score_stock_task
    for each stock.
    """
    logger.info("[SCORE_ALL] Starting batch scoring for all active stocks")

    supabase = get_supabase_client()
    if not supabase:
        logger.error("[SCORE_ALL] Supabase unavailable")
        return {"status": "error", "reason": "supabase_unavailable"}

    try:
        res = (
            supabase.table("stocks")
            .select("id, ticker, sectors(slug)")
            .eq("is_active", True)
            .eq("is_deleted", False)
            .execute()
        )
        stocks = res.data or []
    except Exception as e:
        logger.error(f"[SCORE_ALL] Failed to fetch stocks: {e}")
        return {"status": "error", "reason": str(e)}

    if not stocks:
        logger.warning("[SCORE_ALL] No active stocks found")
        return {"status": "skipped", "reason": "no_active_stocks"}

    dispatched = 0
    for stock in stocks:
        stock_id = stock["id"]
        ticker = stock["ticker"]
        sector_slug = stock.get("sectors", {}).get("slug", "other") if stock.get("sectors") else "other"

        score_stock_task.delay(stock_id=stock_id, ticker=ticker, sector_slug=sector_slug)
        dispatched += 1

    logger.info(f"[SCORE_ALL] Dispatched {dispatched} scoring tasks")
    return {"status": "dispatched", "count": dispatched}


@celery_app.task(name="jobs.scoring_tasks.score_sector_task", bind=True)
def score_sector_task(self, sector_slug: str) -> Dict[str, Any]:
    """
    Score all stocks within a specific sector.
    """
    logger.info(f"[SCORE_SECTOR] Starting scoring for sector: {sector_slug}")

    supabase = get_supabase_client()
    if not supabase:
        return {"status": "error", "reason": "supabase_unavailable"}

    try:
        res = (
            supabase.table("stocks")
            .select("id, ticker, sectors!inner(slug)")
            .eq("sectors.slug", sector_slug)
            .eq("is_active", True)
            .eq("is_deleted", False)
            .execute()
        )
        stocks = res.data or []
    except Exception as e:
        logger.error(f"[SCORE_SECTOR] Failed to fetch stocks for sector {sector_slug}: {e}")
        return {"status": "error", "reason": str(e)}

    dispatched = 0
    for stock in stocks:
        score_stock_task.delay(
            stock_id=stock["id"],
            ticker=stock["ticker"],
            sector_slug=sector_slug,
        )
        dispatched += 1

    logger.info(f"[SCORE_SECTOR] Dispatched {dispatched} tasks for sector {sector_slug}")
    return {"status": "dispatched", "sector": sector_slug, "count": dispatched}
