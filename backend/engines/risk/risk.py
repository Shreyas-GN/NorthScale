"""
engines/risk/risk.py

Deterministic risk scoring engine.
Evaluates leverage, valuation, governance, cyclicality,
earnings volatility, and ownership risks.

All outputs are typed, explainable, and auditable.
Risk penalties reduce conviction scores — never silently ignored.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from engines.models import FinancialMetricsInput, RiskOutput

# ---------------------------------------------------------------------------
# Sector cyclicality baseline — inherent sector risk
# ---------------------------------------------------------------------------

SECTOR_CYCLICALITY: Dict[str, float] = {
    "metals": 4.0,
    "energy": 3.5,
    "auto": 3.0,
    "infrastructure": 3.0,
    "cement": 2.5,
    "banking": 2.5,
    "pharma": 2.0,
    "telecom": 2.0,
    "fmcg": 1.0,
    "it": 1.5,
    "finance": 2.5,
    "conglomerate": 2.0,
    "paints": 1.5,
    "consumer durables": 2.0,
}

DEFAULT_CYCLICALITY = 2.0


# ---------------------------------------------------------------------------
# Individual risk calculators
# ---------------------------------------------------------------------------

def _leverage_risk(
    debt_to_equity: Optional[float],
    interest_coverage: Optional[float],
) -> Tuple[float, List[str]]:
    """
    Leverage Risk — evaluates debt load and debt servicing capacity.
    Penalty: 0–5.0
    """
    penalty = 0.0
    signals: List[str] = []

    if debt_to_equity is None and interest_coverage is None:
        signals.append("Leverage data unavailable — risk not assessable")
        return 2.0, signals  # Conservative default when data missing

    if debt_to_equity is not None:
        if debt_to_equity > 3.0:
            penalty += 4.0
            signals.append(f"Critical leverage: D/E = {debt_to_equity:.2f} (>3.0)")
        elif debt_to_equity > 2.0:
            penalty += 2.5
            signals.append(f"High leverage: D/E = {debt_to_equity:.2f} (>2.0)")
        elif debt_to_equity > 1.0:
            penalty += 1.0
            signals.append(f"Moderate leverage: D/E = {debt_to_equity:.2f} (>1.0)")

    if interest_coverage is not None:
        if interest_coverage < 1.5:
            penalty += 4.0
            signals.append(f"Dangerous interest coverage: {interest_coverage:.2f}x (<1.5x)")
        elif interest_coverage < 2.5:
            penalty += 2.0
            signals.append(f"Weak interest coverage: {interest_coverage:.2f}x (<2.5x)")
        elif interest_coverage < 3.5:
            penalty += 0.5
            signals.append(f"Tight interest coverage: {interest_coverage:.2f}x (<3.5x)")

    return min(5.0, penalty), signals


def _valuation_risk(
    pe_ratio: Optional[float],
    pb_ratio: Optional[float],
    sector_slug: str,
) -> Tuple[float, List[str]]:
    """
    Valuation Risk — sector-aware PE/PB overvaluation risk.
    Penalty: 0–4.0
    """
    penalty = 0.0
    signals: List[str] = []

    if pe_ratio is None and pb_ratio is None:
        return 0.0, signals

    sector = sector_slug.lower()

    # Sector-specific PE thresholds
    pe_thresholds: Dict[str, Tuple[float, float]] = {
        "it": (45.0, 60.0),
        "fmcg": (55.0, 80.0),
        "pharma": (35.0, 55.0),
        "banking": (20.0, 30.0),
        "finance": (25.0, 40.0),
    }
    warn_pe, danger_pe = pe_thresholds.get(sector, (30.0, 50.0))

    if pe_ratio is not None and pe_ratio > 0:
        if pe_ratio > danger_pe:
            penalty += 3.0
            signals.append(f"Dangerously elevated PE: {pe_ratio:.1f}x (>{danger_pe:.0f}x for {sector.upper()})")
        elif pe_ratio > warn_pe:
            penalty += 1.5
            signals.append(f"Elevated PE: {pe_ratio:.1f}x (>{warn_pe:.0f}x for {sector.upper()})")

    if pb_ratio is not None:
        if pb_ratio > 12.0:
            penalty += 2.0
            signals.append(f"Extreme P/B ratio: {pb_ratio:.2f}x (>12.0)")
        elif pb_ratio > 7.0:
            penalty += 0.5
            signals.append(f"High P/B ratio: {pb_ratio:.2f}x (>7.0)")

    return min(4.0, penalty), signals


def _governance_risk(
    promoter_pledge_pct: Optional[float],
    promoter_change_qoq: Optional[float],
) -> Tuple[float, List[str]]:
    """
    Governance Risk — evaluates promoter pledge and selling patterns.
    Penalty: 0–5.0
    """
    penalty = 0.0
    signals: List[str] = []

    if promoter_pledge_pct is not None:
        if promoter_pledge_pct > 40:
            penalty += 5.0
            signals.append(f"Extreme promoter pledge: {promoter_pledge_pct:.1f}% — CRITICAL governance risk")
        elif promoter_pledge_pct > 25:
            penalty += 3.5
            signals.append(f"High promoter pledge: {promoter_pledge_pct:.1f}% (>25%)")
        elif promoter_pledge_pct > 10:
            penalty += 1.5
            signals.append(f"Moderate promoter pledge: {promoter_pledge_pct:.1f}% (>10%)")

    if promoter_change_qoq is not None:
        if promoter_change_qoq < -3.0:
            penalty += 2.5
            signals.append(f"Significant promoter selling: {promoter_change_qoq:.2f}% QoQ reduction")
        elif promoter_change_qoq < -1.0:
            penalty += 1.0
            signals.append(f"Promoter reducing stake: {promoter_change_qoq:.2f}% QoQ")

    return min(5.0, penalty), signals


def _ownership_risk(
    fii_change_qoq: Optional[float],
    dii_change_qoq: Optional[float],
) -> Tuple[float, List[str]]:
    """
    Ownership Risk — evaluates institutional selling pressure.
    Penalty: 0–2.0
    """
    penalty = 0.0
    signals: List[str] = []

    if fii_change_qoq is not None and fii_change_qoq < -5.0:
        penalty += 1.5
        signals.append(f"Heavy FII selling: {fii_change_qoq:.2f}% QoQ reduction")
    elif fii_change_qoq is not None and fii_change_qoq < -2.0:
        penalty += 0.5
        signals.append(f"FII reducing position: {fii_change_qoq:.2f}% QoQ")

    if dii_change_qoq is not None and dii_change_qoq < -5.0:
        penalty += 0.5
        signals.append(f"DII selling pressure: {dii_change_qoq:.2f}% QoQ")

    return min(2.0, penalty), signals


def _cyclicality_risk(sector_slug: str) -> Tuple[float, List[str]]:
    """
    Cyclicality Risk — inherent sector cyclicality baseline.
    Penalty: 1.0–4.0
    """
    risk = SECTOR_CYCLICALITY.get(sector_slug.lower(), DEFAULT_CYCLICALITY)
    if risk >= 3.5:
        return risk, [f"{sector_slug.upper()} is a highly cyclical sector — earnings volatile with macro cycles"]
    if risk >= 2.5:
        return risk, [f"{sector_slug.upper()} exhibits moderate cyclicality"]
    return risk, []


def _earnings_volatility_risk(
    revenue_1y_growth: Optional[float],
    profit_1y_growth: Optional[float],
    revenue_3y_cagr: Optional[float],
    profit_3y_cagr: Optional[float],
) -> Tuple[float, List[str]]:
    """
    Earnings Volatility Risk — compares short-term vs long-term growth.
    Penalty: 0–3.0
    """
    penalty = 0.0
    signals: List[str] = []

    # If profit grew much faster than revenue recently, it may be unsustainable
    if (
        profit_1y_growth is not None
        and revenue_1y_growth is not None
        and profit_1y_growth > revenue_1y_growth + 30
    ):
        penalty += 1.0
        signals.append("Profit growth significantly outpacing revenue — sustainability risk")

    # Negative recent growth despite positive CAGR = deterioration
    if profit_1y_growth is not None and profit_1y_growth < -10:
        penalty += 2.5
        signals.append(f"Significant profit decline: {profit_1y_growth:.1f}% YoY")
    elif profit_1y_growth is not None and profit_1y_growth < 0:
        penalty += 1.0
        signals.append(f"Profit contraction: {profit_1y_growth:.1f}% YoY")

    if revenue_1y_growth is not None and revenue_1y_growth < -5:
        penalty += 1.5
        signals.append(f"Revenue contraction: {revenue_1y_growth:.1f}% YoY")

    return min(3.0, penalty), signals


# ---------------------------------------------------------------------------
# Composite risk evaluator
# ---------------------------------------------------------------------------

def evaluate_total_risk(
    metrics: FinancialMetricsInput,
    sector_slug: str,
) -> RiskOutput:
    """
    Run all risk sub-engines and aggregate into a typed RiskOutput.
    Each sub-engine contributes a penalty (0–N) and explainable signals.
    """
    all_signals: List[str] = []

    lev_penalty, lev_signals = _leverage_risk(metrics.debt_to_equity, metrics.interest_coverage)
    all_signals.extend(lev_signals)

    val_penalty, val_signals = _valuation_risk(metrics.pe_ratio, metrics.pb_ratio, sector_slug)
    all_signals.extend(val_signals)

    gov_penalty, gov_signals = _governance_risk(
        metrics.promoter_pledge_pct, metrics.promoter_change_qoq
    )
    all_signals.extend(gov_signals)

    own_penalty, own_signals = _ownership_risk(metrics.fii_change_qoq, metrics.dii_change_qoq)
    all_signals.extend(own_signals)

    cyc_penalty, cyc_signals = _cyclicality_risk(sector_slug)
    all_signals.extend(cyc_signals)

    vol_penalty, vol_signals = _earnings_volatility_risk(
        metrics.revenue_1y_growth,
        metrics.profit_1y_growth,
        metrics.revenue_3y_cagr,
        metrics.profit_3y_cagr,
    )
    all_signals.extend(vol_signals)

    # Aggregate total penalty (capped at 10 — we don't punish beyond max)
    total = lev_penalty + val_penalty + gov_penalty + own_penalty + cyc_penalty * 0.3 + vol_penalty

    return RiskOutput(
        leverage_risk=lev_penalty,
        valuation_risk=val_penalty,
        governance_risk=gov_penalty,
        ownership_risk=own_penalty,
        cyclicality_risk=round(cyc_penalty, 2),
        earnings_volatility_risk=vol_penalty,
        total_risk_penalty=round(min(10.0, total), 4),
        risk_signals=all_signals,
    )
