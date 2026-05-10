"""
engines/sectors/registry.py

Sector scorer registry — maps sector slugs to their scorer implementations.
Provides a fallback generic scorer for sectors without a dedicated implementation.
"""

from __future__ import annotations

from typing import Optional

from engines.sectors.base import BaseSectorScorer
from engines.sectors.it import ITScorer
from engines.sectors.banking import BankingScorer
from engines.sectors.fmcg import FMCGScorer
from engines.sectors.pharma import PharmaScorer
from engines.sectors.infrastructure import InfraScorer

# Alias slugs that share the same scorer
_REGISTRY: dict[str, BaseSectorScorer] = {
    "it": ITScorer(),
    "banking": BankingScorer(),
    "finance": BankingScorer(),   # Finance sector uses banking scorer
    "fmcg": FMCGScorer(),
    "pharma": PharmaScorer(),
    "infrastructure": InfraScorer(),
    "cement": InfraScorer(),      # Cement uses infra scorer (capex-heavy, leverage)
}


def get_sector_scorer(sector_slug: str) -> Optional[BaseSectorScorer]:
    """
    Return the appropriate sector scorer for a given slug.
    Returns None for unknown sectors (pipeline will use generic fallback).
    """
    return _REGISTRY.get(sector_slug.lower().strip())
