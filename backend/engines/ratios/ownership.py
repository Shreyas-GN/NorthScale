"""
engines/ratios/ownership.py

Deterministic ownership quality metrics.
Evaluates promoter conviction, institutional confidence, and ownership stability.
"""

from __future__ import annotations

from typing import Optional

from engines.models import FinancialMetricsInput, OwnershipMetrics


def calculate_promoter_holding_trend(
    current: Optional[float],
    previous: Optional[float],
) -> Optional[float]:
    """
    QoQ change in promoter holding (percentage points).
    Positive = increasing conviction, Negative = potential concern.
    """
    if current is None or previous is None:
        return None
    return round(current - previous, 4)


def classify_promoter_pledge_risk(pledge_pct: Optional[float]) -> str:
    """
    Classify promoter pledge level.
    Returns: 'NONE', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL'
    """
    if pledge_pct is None:
        return "UNKNOWN"
    if pledge_pct == 0:
        return "NONE"
    if pledge_pct < 5:
        return "LOW"
    if pledge_pct < 15:
        return "MODERATE"
    if pledge_pct < 25:
        return "HIGH"
    return "CRITICAL"


def extract_ownership_metrics(metrics: FinancialMetricsInput) -> OwnershipMetrics:
    """Extract ownership metrics from a normalized snapshot."""
    return OwnershipMetrics(
        promoter_holding=metrics.promoter_holding,
        promoter_pledge_pct=metrics.promoter_pledge_pct,
        promoter_change_qoq=metrics.promoter_change_qoq,
        fii_holding=metrics.fii_holding,
        fii_change_qoq=metrics.fii_change_qoq,
        dii_holding=metrics.dii_holding,
        dii_change_qoq=metrics.dii_change_qoq,
    )
