"""
engines/pipeline.py

Deterministic Scoring Pipeline — Entry Point.

Orchestrates the full Phase 3 intelligence pipeline:

  FinancialMetricsInput
         ↓
  Sector Classification (registry lookup)
         ↓
  Category Scoring (5 categories via sector scorer)
         ↓
  Risk Evaluation (6 risk sub-engines)
         ↓
  Conviction Calculation (risk-adjusted composite)
         ↓
  Recommendation Classification (threshold-based)
         ↓
  Explainability Assembly (full factor attribution)
         ↓
  ScoringResult (auditable, typed output)

Every step is deterministic, typed, and traceable.
No AI. No randomness. No hallucination.
"""

from __future__ import annotations

from datetime import date

from core.logging import logger

from engines.conviction import compute_conviction
from engines.explainability import build_explainability
from engines.models import (
    CategoryScore,
    FinancialMetricsInput,
    RecommendationCategory,
    ScoringResult,
)
from engines.recommendation.engine import classify_recommendation
from engines.risk.risk import evaluate_total_risk
from engines.sectors.registry import get_sector_scorer

SCORING_VERSION = "1.0.0"


def _generic_category_scores(metrics: FinancialMetricsInput) -> list[CategoryScore]:
    """
    Fallback generic scorer for sectors without a dedicated implementation.
    Uses the base weight model from SCORING_ENGINE.md.
    """
    default_weights = {
        "growth": 0.25,
        "profitability": 0.20,
        "valuation": 0.20,
        "financial_health": 0.20,
        "ownership": 0.10,
    }
    results = []

    # Growth
    g_score = 0.0
    g_pos, g_neg = [], []
    if metrics.revenue_3y_cagr is not None:
        if metrics.revenue_3y_cagr >= 15:
            g_score = 8.0; g_pos.append(f"Revenue CAGR: {metrics.revenue_3y_cagr:.1f}%")
        elif metrics.revenue_3y_cagr >= 10:
            g_score = 6.0; g_pos.append(f"Revenue CAGR: {metrics.revenue_3y_cagr:.1f}%")
        elif metrics.revenue_3y_cagr >= 5:
            g_score = 4.0
        else:
            g_score = 1.0; g_neg.append(f"Low revenue CAGR: {metrics.revenue_3y_cagr:.1f}%")

    w = default_weights["growth"]
    results.append(CategoryScore(
        category="growth", raw_score=g_score, weight=w,
        weighted_contribution=round(g_score * w, 4),
        positive_signals=g_pos, negative_signals=g_neg,
        data_available=metrics.revenue_3y_cagr is not None,
    ))

    # Profitability
    p_score = 0.0
    p_pos, p_neg = [], []
    if metrics.roce is not None:
        if metrics.roce >= 20: p_score = 8.0; p_pos.append(f"ROCE: {metrics.roce:.1f}%")
        elif metrics.roce >= 12: p_score = 5.0; p_pos.append(f"ROCE: {metrics.roce:.1f}%")
        else: p_score = 2.0; p_neg.append(f"Weak ROCE: {metrics.roce:.1f}%")

    w = default_weights["profitability"]
    results.append(CategoryScore(
        category="profitability", raw_score=p_score, weight=w,
        weighted_contribution=round(p_score * w, 4),
        positive_signals=p_pos, negative_signals=p_neg,
        data_available=metrics.roce is not None,
    ))

    # Valuation
    v_score = 0.0
    v_pos, v_neg = [], []
    if metrics.pe_ratio is not None and metrics.pe_ratio > 0:
        if metrics.pe_ratio < 20: v_score = 9.0; v_pos.append(f"PE: {metrics.pe_ratio:.1f}x")
        elif metrics.pe_ratio < 30: v_score = 7.0; v_pos.append(f"PE: {metrics.pe_ratio:.1f}x")
        elif metrics.pe_ratio < 45: v_score = 4.0
        else: v_score = 1.0; v_neg.append(f"High PE: {metrics.pe_ratio:.1f}x")

    w = default_weights["valuation"]
    results.append(CategoryScore(
        category="valuation", raw_score=v_score, weight=w,
        weighted_contribution=round(v_score * w, 4),
        positive_signals=v_pos, negative_signals=v_neg,
        data_available=metrics.pe_ratio is not None,
    ))

    # Financial Health
    fh_score = 0.0
    fh_pos, fh_neg = [], []
    if metrics.debt_to_equity is not None:
        if metrics.debt_to_equity < 0.5: fh_score = 9.0; fh_pos.append(f"Low D/E: {metrics.debt_to_equity:.2f}")
        elif metrics.debt_to_equity < 1.0: fh_score = 6.0
        elif metrics.debt_to_equity < 2.0: fh_score = 3.0
        else: fh_score = 0.0; fh_neg.append(f"High D/E: {metrics.debt_to_equity:.2f}")

    w = default_weights["financial_health"]
    results.append(CategoryScore(
        category="financial_health", raw_score=fh_score, weight=w,
        weighted_contribution=round(fh_score * w, 4),
        positive_signals=fh_pos, negative_signals=fh_neg,
        data_available=metrics.debt_to_equity is not None,
    ))

    # Ownership
    o_score = 0.0
    o_pos, o_neg = [], []
    if metrics.promoter_holding is not None:
        if metrics.promoter_holding >= 55: o_score = 9.0; o_pos.append(f"Promoter: {metrics.promoter_holding:.1f}%")
        elif metrics.promoter_holding >= 40: o_score = 6.0
        else: o_score = 3.0; o_neg.append(f"Low promoter: {metrics.promoter_holding:.1f}%")

    if metrics.promoter_pledge_pct == 0:
        o_score += 1.0; o_pos.append("Zero pledge")
    elif metrics.promoter_pledge_pct and metrics.promoter_pledge_pct > 15:
        o_score -= 2.0; o_neg.append(f"Pledge: {metrics.promoter_pledge_pct:.1f}%")

    o_score = max(0.0, min(10.0, o_score))
    w = default_weights["ownership"]
    results.append(CategoryScore(
        category="ownership", raw_score=o_score, weight=w,
        weighted_contribution=round(o_score * w, 4),
        positive_signals=o_pos, negative_signals=o_neg,
        data_available=metrics.promoter_holding is not None,
    ))

    return results


def run_scoring_pipeline(metrics: FinancialMetricsInput) -> ScoringResult:
    """
    Execute the full deterministic scoring pipeline for a single stock.

    Steps:
      1. Get sector-specific scorer (or use generic fallback)
      2. Score all 5 categories
      3. Evaluate all 6 risk dimensions
      4. Compute risk-adjusted conviction
      5. Classify recommendation
      6. Build explainability
      7. Return typed ScoringResult

    This is the single entry point for the intelligence engine.
    """
    ticker = metrics.ticker
    sector = metrics.sector_slug

    logger.info(f"[PIPELINE] Running scoring pipeline for {ticker} | sector={sector}")

    # Step 1: Sector scorer
    scorer = get_sector_scorer(sector)
    if scorer:
        logger.debug(f"[PIPELINE] Using {scorer.sector_name} scorer for {ticker}")
        category_scores = scorer.score_all(metrics)
    else:
        logger.warning(f"[PIPELINE] No dedicated scorer for sector '{sector}' — using generic fallback")
        category_scores = _generic_category_scores(metrics)

    # Step 2: Risk evaluation
    risk_output = evaluate_total_risk(metrics, sector)
    logger.debug(
        f"[PIPELINE] {ticker} risk: penalty={risk_output.total_risk_penalty:.2f} | "
        f"signals={len(risk_output.risk_signals)}"
    )

    # Step 3: Conviction
    conviction = compute_conviction(category_scores, risk_output, metrics)
    logger.info(
        f"[PIPELINE] {ticker} conviction={conviction.conviction_score:.2f} | "
        f"tier={conviction.conviction_tier.value} | confidence={conviction.confidence_level.value}"
    )

    # Step 4: Recommendation classification
    recommendation = classify_recommendation(conviction)
    logger.info(f"[PIPELINE] {ticker} → {recommendation.value}")

    # Step 5: Explainability
    explainability = build_explainability(
        category_scores=category_scores,
        risk_output=risk_output,
        conviction=conviction,
        metrics=metrics,
        sector_slug=sector,
    )

    # Step 6: Extract individual category scores for DB storage
    cat_map = {cs.category: cs.raw_score for cs in category_scores}

    return ScoringResult(
        stock_id=metrics.stock_id,
        ticker=ticker,
        sector_slug=sector,
        snapshot_date=metrics.snapshot_date,
        recommendation=recommendation,
        conviction=conviction,
        explainability=explainability,
        growth_score=cat_map.get("growth"),
        profitability_score=cat_map.get("profitability"),
        valuation_score=cat_map.get("valuation"),
        financial_health_score=cat_map.get("financial_health"),
        ownership_score=cat_map.get("ownership"),
        risk_score=round(risk_output.total_risk_penalty, 2),
        composite_score=conviction.composite_score,
        financial_snapshot_id=metrics.financial_snapshot_id,
        ownership_snapshot_id=metrics.ownership_snapshot_id,
        scoring_version=SCORING_VERSION,
    )
