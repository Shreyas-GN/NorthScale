"""
services/recommendation_service.py

Recommendation persistence service.

Handles:
  - Upsert of current active recommendation (recommendations table)
  - Append-only insert to recommendation_history (never update)
  - Structured, auditable DB writes

All writes are typed and based on ScoringResult.
No overwriting of historical records — ever.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from core.logging import logger
from db.supabase import get_supabase_client
from engines.models import ScoringResult


class RecommendationService:
    """
    Manages persistence of scoring results to Supabase.
    Implements the append-only historical snapshot strategy.
    """

    def __init__(self) -> None:
        self.supabase = get_supabase_client()

    def _ensure_client(self) -> None:
        if not self.supabase:
            raise RuntimeError("Supabase client not initialized.")

    def upsert_recommendation(self, result: ScoringResult) -> Optional[str]:
        """
        Upsert the current active recommendation for a stock.
        Only one active recommendation per stock (UNIQUE on stock_id).
        Returns the recommendation UUID or None on failure.
        """
        self._ensure_client()

        payload: Dict[str, Any] = {
            "stock_id": result.stock_id,
            "recommendation": result.recommendation.value,
            "conviction_score": float(result.conviction.conviction_score),
            "confidence_level": result.conviction.confidence_level.value,
            "growth_score": result.growth_score,
            "profitability_score": result.profitability_score,
            "valuation_score": result.valuation_score,
            "financial_health_score": result.financial_health_score,
            "ownership_score": result.ownership_score,
            "risk_score": result.risk_score,
            "composite_score": float(result.composite_score),
            "financial_snapshot_id": result.financial_snapshot_id,
            "ownership_snapshot_id": result.ownership_snapshot_id,
            "generated_at": result.generated_at.isoformat(),
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            res = (
                self.supabase.table("recommendations")
                .upsert(payload, on_conflict="stock_id")
                .execute()
            )
            if res.data:
                rec_id = res.data[0].get("id")
                logger.info(
                    f"[REC_SERVICE] Upserted recommendation for {result.ticker}: "
                    f"{result.recommendation.value} (conviction={result.conviction.conviction_score:.2f})"
                )
                return rec_id
            return None
        except Exception as e:
            logger.error(f"[REC_SERVICE] Failed to upsert recommendation for {result.ticker}: {e}")
            return None

    def append_recommendation_history(
        self,
        result: ScoringResult,
        recommendation_id: Optional[str],
        previous_recommendation: Optional[str] = None,
        change_reason: Optional[str] = None,
    ) -> bool:
        """
        Insert an immutable historical snapshot into recommendation_history.
        This record is NEVER updated — only inserted.
        Supports full auditability and conviction drift analysis.
        """
        self._ensure_client()

        payload: Dict[str, Any] = {
            "stock_id": result.stock_id,
            "recommendation_id": recommendation_id,
            "recommendation": result.recommendation.value,
            "conviction_score": float(result.conviction.conviction_score),
            "confidence_level": result.conviction.confidence_level.value,
            "growth_score": result.growth_score,
            "profitability_score": result.profitability_score,
            "valuation_score": result.valuation_score,
            "financial_health_score": result.financial_health_score,
            "ownership_score": result.ownership_score,
            "risk_score": result.risk_score,
            "composite_score": float(result.composite_score),
            "previous_recommendation": previous_recommendation,
            "change_reason": change_reason,
            "financial_snapshot_id": result.financial_snapshot_id,
            "generated_at": result.generated_at.isoformat(),
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            self.supabase.table("recommendation_history").insert(payload).execute()
            logger.info(
                f"[REC_SERVICE] Appended history for {result.ticker} "
                f"({result.recommendation.value}, conviction={result.conviction.conviction_score:.2f})"
            )
            return True
        except Exception as e:
            logger.error(f"[REC_SERVICE] Failed to append history for {result.ticker}: {e}")
            return False

    def get_previous_recommendation(self, stock_id: str) -> Optional[str]:
        """
        Fetch the last active recommendation value for a stock.
        Used to detect recommendation changes in historical tracking.
        """
        self._ensure_client()
        try:
            res = (
                self.supabase.table("recommendations")
                .select("recommendation")
                .eq("stock_id", stock_id)
                .maybe_single()
                .execute()
            )
            if res.data:
                return res.data.get("recommendation")
            return None
        except Exception as e:
            logger.warning(f"[REC_SERVICE] Could not fetch previous recommendation for {stock_id}: {e}")
            return None

    def persist_scoring_result(self, result: ScoringResult) -> bool:
        """
        Full persistence flow:
          1. Get previous recommendation (for change detection)
          2. Upsert current recommendation
          3. Append historical snapshot

        Returns True if both writes succeeded.
        """
        previous = self.get_previous_recommendation(result.stock_id)

        change_reason = None
        if previous and previous != result.recommendation.value:
            change_reason = (
                f"Recommendation changed from {previous} to {result.recommendation.value} "
                f"(conviction: {result.conviction.conviction_score:.2f}, "
                f"confidence: {result.conviction.confidence_level.value})"
            )
            logger.info(f"[REC_SERVICE] Recommendation CHANGED for {result.ticker}: {previous} → {result.recommendation.value}")

        rec_id = self.upsert_recommendation(result)
        history_ok = self.append_recommendation_history(
            result=result,
            recommendation_id=rec_id,
            previous_recommendation=previous,
            change_reason=change_reason,
        )

        return rec_id is not None and history_ok
