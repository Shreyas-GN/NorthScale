"""
engines/benchmarks.py

Benchmark Comparison Engine.

Compares a stock's financial metrics against sector medians.
Provides deterministic scoring adjustments based on relative performance.
"""

from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel
from engines.models import FinancialMetricsInput

class SectorBenchmark(BaseModel):
    sector_id: str
    median_pe: Optional[float] = None
    median_pb: Optional[float] = None
    median_roe: Optional[float] = None
    median_roce: Optional[float] = None
    median_revenue_growth: Optional[float] = None
    median_profit_growth: Optional[float] = None

class BenchmarkComparison(BaseModel):
    pe_vs_median: Optional[float] = None
    roe_vs_median: Optional[float] = None
    growth_vs_median: Optional[float] = None
    is_outperformer: bool = False

def compare_to_benchmark(metrics: FinancialMetricsInput, benchmark: SectorBenchmark) -> BenchmarkComparison:
    """
    Compare stock metrics to sector benchmarks.
    Returns relative performance metrics.
    """
    pe_rel = None
    if metrics.pe_ratio and benchmark.median_pe:
        pe_rel = metrics.pe_ratio / benchmark.median_pe

    roe_rel = None
    if metrics.roe and benchmark.median_roe:
        roe_rel = metrics.roe - benchmark.median_roe

    growth_rel = None
    if metrics.revenue_3y_cagr and benchmark.median_revenue_growth:
        growth_rel = metrics.revenue_3y_cagr - benchmark.median_revenue_growth

    # Deterministic outperformer logic
    outperformer = False
    if roe_rel and roe_rel > 5 and growth_rel and growth_rel > 0:
        outperformer = True

    return BenchmarkComparison(
        pe_vs_median=pe_rel,
        roe_vs_median=roe_rel,
        growth_vs_median=growth_rel,
        is_outperformer=outperformer
    )
