"""
ai/generators/portfolio_generator.py

AI Portfolio Intelligence Generator.
Analyzes portfolio holdings based on deterministic signals.
Provides concentration warnings and sector overexposure alerts.
"""

import json
from typing import Dict, Any, List

from ai.groq_client import GroqClient, ModelLiteral
from ai.prompt_builder import PROMPT_VERSION
from core.logging import logger

class PortfolioGenerator:
    def __init__(self):
        self.groq_client = GroqClient()

    def _build_system_prompt(self) -> str:
        return f"""You are NorthScale AI, an institutional-grade portfolio analyst.
Your task is to analyze portfolio holdings based strictly on deterministic signals.

PROMPT_VERSION: {PROMPT_VERSION}

CRITICAL RULES:
1. Provide portfolio insights derived from deterministic scores only.
2. No speculative financial advice.
3. Outputs must be explainable and based purely on the provided data.
4. Output MUST be a valid JSON object.
"""

    def _build_user_prompt(self, portfolio_data: Dict[str, Any]) -> str:
        return f"""
Please generate portfolio intelligence based on the following portfolio data and underlying stock metrics.

PORTFOLIO DATA:
{json.dumps(portfolio_data, indent=2)}

OUTPUT FORMAT:
{{
  "ai_summary": "A concise 2-sentence summary of the portfolio's overall health.",
  "risk_summary": "A summary of key portfolio-level risks.",
  "alerts": [
    "String alert 1",
    "String alert 2"
  ]
}}
"""

    def generate_portfolio_intelligence(self, portfolio_data: Dict[str, Any], model: ModelLiteral = "mixtral-8x7b-32768") -> Dict[str, Any]:
        """
        Generate portfolio intelligence.
        """
        logger.info(f"[PORTFOLIO_GEN] Generating portfolio intelligence using {model}")
        
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(portfolio_data)

        try:
            response = self.groq_client.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=model,
                response_format={"type": "json_object"}
            )
            
            data = json.loads(response.content)
            
            # Simple validation
            if "ai_summary" not in data or "risk_summary" not in data:
                raise ValueError("Missing required fields in portfolio output")
                
            return data
            
        except Exception as e:
            logger.error(f"[PORTFOLIO_GEN] Portfolio generation error: {e}")
            return {
                "ai_summary": "Portfolio analysis is currently unavailable.",
                "risk_summary": "Unable to calculate portfolio risk.",
                "alerts": [],
                "is_fallback": True
            }
