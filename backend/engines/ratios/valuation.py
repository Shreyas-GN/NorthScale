"""
engines/ratios/valuation.py

Deterministic valuation ratio calculations.
All functions are pure, typed, and handle None/invalid data gracefully.
"""

from __future__ import annotations

from typing import Optional

from engines.models import FinancialMetricsInput, ValuationRatios


def calculate_pe(price: Optional[float], eps: Optional[float]) -> Optional[float]:
    """Price-to-Earnings = Price / EPS (TTM)"""
    if price is None or eps is None or eps <= 0:
        return None
    return round(price / eps, 4)


def calculate_pb(price: Optional[float], bvps: Optional[float]) -> Optional[float]:
    """Price-to-Book = Price / Book Value Per Share"""
    if price is None or bvps is None or bvps <= 0:
        return None
    return round(price / bvps, 4)


def calculate_ev_ebitda(ev: Optional[float], ebitda: Optional[float]) -> Optional[float]:
    """EV/EBITDA = Enterprise Value / EBITDA"""
    if ev is None or ebitda is None or ebitda <= 0:
        return None
    return round(ev / ebitda, 4)


def calculate_price_to_sales(market_cap: Optional[float], revenue_ttm: Optional[float]) -> Optional[float]:
    """Price-to-Sales = Market Cap / Revenue (TTM)"""
    if market_cap is None or revenue_ttm is None or revenue_ttm <= 0:
        return None
    return round(market_cap / revenue_ttm, 4)


def extract_valuation_ratios(metrics: FinancialMetricsInput) -> ValuationRatios:
    """Extract valuation ratios from a normalized snapshot."""
    return ValuationRatios(
        pe_ratio=metrics.pe_ratio,
        pb_ratio=metrics.pb_ratio,
        ev_to_ebitda=metrics.ev_to_ebitda,
        price_to_sales=metrics.price_to_sales,
    )
