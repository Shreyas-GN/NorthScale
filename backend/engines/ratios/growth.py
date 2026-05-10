"""
engines/ratios/growth.py

Deterministic growth ratio calculations.
CAGR formula: (End / Start) ^ (1/years) - 1
"""

from __future__ import annotations

from typing import Optional

from engines.models import FinancialMetricsInput, GrowthRatios


def calculate_cagr(
    start_value: Optional[float],
    end_value: Optional[float],
    years: int,
) -> Optional[float]:
    """
    Compound Annual Growth Rate (CAGR).
    Returns percentage (e.g. 12.5 for 12.5%).
    Returns None if inputs are invalid.
    """
    if start_value is None or end_value is None:
        return None
    if years <= 0:
        return None
    if start_value <= 0:
        return None  # Cannot compute CAGR from zero or negative base
    return round(((end_value / start_value) ** (1 / years) - 1) * 100, 4)


def calculate_yoy_growth(
    current: Optional[float],
    previous: Optional[float],
) -> Optional[float]:
    """
    Year-over-Year growth rate.
    Returns percentage.
    """
    if current is None or previous is None or previous <= 0:
        return None
    return round(((current - previous) / previous) * 100, 4)


def extract_growth_ratios(metrics: FinancialMetricsInput) -> GrowthRatios:
    """Extract pre-computed growth ratios from a normalized snapshot."""
    return GrowthRatios(
        revenue_1y_growth=metrics.revenue_1y_growth,
        revenue_3y_cagr=metrics.revenue_3y_cagr,
        revenue_5y_cagr=metrics.revenue_5y_cagr,
        profit_1y_growth=metrics.profit_1y_growth,
        profit_3y_cagr=metrics.profit_3y_cagr,
        profit_5y_cagr=metrics.profit_5y_cagr,
    )
