"""
engines/ratios/profitability.py

Deterministic profitability ratio calculations.
All functions are pure, typed, and handle None gracefully.
"""

from __future__ import annotations

from typing import Optional

from engines.models import FinancialMetricsInput, ProfitabilityRatios


def calculate_roe(net_profit: Optional[float], equity: Optional[float]) -> Optional[float]:
    """Return On Equity = (Net Profit / Shareholders' Equity) * 100"""
    if net_profit is None or equity is None or equity <= 0:
        return None
    return round((net_profit / equity) * 100, 4)


def calculate_roce(ebit: Optional[float], capital_employed: Optional[float]) -> Optional[float]:
    """Return On Capital Employed = (EBIT / Capital Employed) * 100"""
    if ebit is None or capital_employed is None or capital_employed <= 0:
        return None
    return round((ebit / capital_employed) * 100, 4)


def calculate_operating_margin(operating_profit: Optional[float], revenue: Optional[float]) -> Optional[float]:
    """Operating Margin = (Operating Profit / Revenue) * 100"""
    if operating_profit is None or revenue is None or revenue <= 0:
        return None
    return round((operating_profit / revenue) * 100, 4)


def calculate_net_margin(net_profit: Optional[float], revenue: Optional[float]) -> Optional[float]:
    """Net Profit Margin = (Net Profit / Revenue) * 100"""
    if net_profit is None or revenue is None or revenue <= 0:
        return None
    return round((net_profit / revenue) * 100, 4)


def extract_profitability_ratios(metrics: FinancialMetricsInput) -> ProfitabilityRatios:
    """
    Extract and validate profitability ratios from a FinancialMetricsInput snapshot.
    Passthrough — these ratios are pre-calculated by the scraper/normalizer.
    """
    return ProfitabilityRatios(
        roe=metrics.roe,
        roce=metrics.roce,
        operating_margin=metrics.operating_margin,
        net_margin=metrics.net_profit_margin,
        ebitda_margin=metrics.ebitda_margin,
    )
