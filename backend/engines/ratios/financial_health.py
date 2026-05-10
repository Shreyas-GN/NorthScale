"""
engines/ratios/financial_health.py

Deterministic financial health ratio calculations.
Evaluates balance sheet quality, debt sustainability, and cash flow strength.
"""

from __future__ import annotations

from typing import Optional

from engines.models import FinancialMetricsInput, FinancialHealthRatios


def calculate_debt_equity(
    total_debt: Optional[float],
    total_equity: Optional[float],
) -> Optional[float]:
    """Debt-to-Equity = Total Debt / Total Shareholders' Equity"""
    if total_debt is None or total_equity is None or total_equity <= 0:
        return None
    return round(total_debt / total_equity, 4)


def calculate_interest_coverage(
    ebit: Optional[float],
    interest_expense: Optional[float],
) -> Optional[float]:
    """Interest Coverage Ratio = EBIT / Interest Expense"""
    if ebit is None or interest_expense is None or interest_expense <= 0:
        return None
    return round(ebit / interest_expense, 4)


def calculate_fcf_quality(
    free_cash_flow: Optional[float],
    net_profit: Optional[float],
) -> Optional[float]:
    """
    FCF Quality = Free Cash Flow / Net Profit.
    Ratio > 1.0 indicates high-quality earnings.
    Ratio < 0.5 indicates poor cash conversion.
    """
    if free_cash_flow is None or net_profit is None or net_profit <= 0:
        return None
    return round(free_cash_flow / net_profit, 4)


def extract_financial_health_ratios(metrics: FinancialMetricsInput) -> FinancialHealthRatios:
    """Extract and compute financial health ratios from a normalized snapshot."""
    fcf_quality = calculate_fcf_quality(metrics.free_cash_flow, metrics.net_profit_ttm)
    return FinancialHealthRatios(
        debt_to_equity=metrics.debt_to_equity,
        current_ratio=metrics.current_ratio,
        interest_coverage=metrics.interest_coverage,
        fcf_quality=fcf_quality,
    )
