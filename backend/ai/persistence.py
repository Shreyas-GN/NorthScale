"""
ai/persistence.py

Database persistence for AI layer.
Handles logging to ai_generation_logs, saving ai_theses and ai_insights.
"""

from typing import Any, Dict, List, Optional
import json

from core.logging import logger
from db.supabase import get_supabase_client
from engines.models import ScoringResult
from ai.groq_client import GroqResponse

class AIPersistence:
    def __init__(self):
        self.supabase = get_supabase_client()

    def _ensure_client(self) -> None:
        if not self.supabase:
            raise RuntimeError("Supabase client not initialized.")

    def log_generation(
        self,
        context_type: str,
        stock_id: str,
        model_id: str,
        status: str,
        prompt_version: str,
        latency_ms: Optional[int] = None,
        input_token_count: Optional[int] = None,
        output_token_count: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """Logs the AI generation attempt to ai_generation_logs."""
        try:
            self._ensure_client()
            payload = {
                "context_type": context_type,
                "stock_id": stock_id,
                "model_id": model_id,
                "status": status,
                "prompt_version": prompt_version,
                "latency_ms": latency_ms,
                "input_token_count": input_token_count,
                "output_token_count": output_token_count,
                "error_message": error_message
            }
            # Remove None values
            payload = {k: v for k, v in payload.items() if v is not None}
            self.supabase.table("ai_generation_logs").insert(payload).execute()
            return True
        except Exception as e:
            logger.error(f"[AI_PERSISTENCE] Failed to log generation: {e}")
            return False

    def save_thesis(
        self,
        result: ScoringResult,
        thesis_data: Dict[str, Any],
        model_id: str,
        prompt_version: str,
        latency_ms: Optional[int] = None,
        input_token_count: Optional[int] = None,
        output_token_count: Optional[int] = None,
        is_fallback: bool = False
    ) -> bool:
        """Saves generated thesis to ai_theses."""
        try:
            self._ensure_client()
            
            # Fetch the active recommendation_id
            rec_res = self.supabase.table("recommendations").select("id").eq("stock_id", result.stock_id).execute()
            recommendation_id = rec_res.data[0]["id"] if rec_res.data else None

            payload = {
                "stock_id": result.stock_id,
                "recommendation_id": recommendation_id,
                "financial_snapshot_id": result.financial_snapshot_id,
                
                "thesis_summary": thesis_data.get("thesis_summary", ""),
                "business_quality": thesis_data.get("business_quality"),
                "key_strengths": thesis_data.get("bullish_factors", []),
                "key_risks": thesis_data.get("bearish_factors", []),
                "valuation_perspective": thesis_data.get("valuation_summary"),
                "overall_view": thesis_data.get("overall_view"),
                
                "model_id": model_id,
                "prompt_version": prompt_version,
                "input_token_count": input_token_count,
                "output_token_count": output_token_count,
                "generation_latency_ms": latency_ms,
                
                "is_fallback": is_fallback,
                "confidence_note": "Fallback triggered." if is_fallback else None
            }
            payload = {k: v for k, v in payload.items() if v is not None}
            self.supabase.table("ai_theses").insert(payload).execute()
            logger.info(f"[AI_PERSISTENCE] Saved thesis for {result.ticker}")
            return True
        except Exception as e:
            logger.error(f"[AI_PERSISTENCE] Failed to save thesis for {result.ticker}: {e}")
            return False

    def save_insights(
        self,
        stock_id: str,
        insights_data: List[Dict[str, Any]],
        model_id: str
    ) -> bool:
        """Saves generated insights to ai_insights."""
        try:
            self._ensure_client()
            payloads = []
            for insight in insights_data:
                payloads.append({
                    "stock_id": stock_id,
                    "insight_type": insight["insight_type"],
                    "title": insight["title"],
                    "body": insight["body"],
                    "severity": insight["severity"],
                    "model_id": model_id
                })
            
            if payloads:
                self.supabase.table("ai_insights").insert(payloads).execute()
                logger.info(f"[AI_PERSISTENCE] Saved {len(payloads)} insights for stock {stock_id}")
            return True
        except Exception as e:
            logger.error(f"[AI_PERSISTENCE] Failed to save insights for {stock_id}: {e}")
            return False
