"""
ai/generators/insights_generator.py

AI Insights Generator.
Generates concise, contextual insights from deterministic signals.
"""

from typing import List, Dict, Any

from engines.models import ScoringResult
from ai.groq_client import GroqClient, ModelLiteral
from ai.prompt_builder import PromptBuilder, PROMPT_VERSION
from ai.validators.output_validator import validate_insights_json
from ai.fallback import build_insights_fallback
from ai.persistence import AIPersistence
from core.logging import logger

class InsightsGenerator:
    def __init__(self):
        self.groq_client = GroqClient()
        self.prompt_builder = PromptBuilder()
        self.persistence = AIPersistence()

    def generate_insights(self, result: ScoringResult, model: ModelLiteral = "mixtral-8x7b-32768") -> List[Dict[str, Any]]:
        """
        Generate, validate, and persist AI insights.
        Uses a faster model (e.g., mixtral) by default for insights.
        """
        logger.info(f"[INSIGHTS_GEN] Generating insights for {result.ticker} using {model}")
        
        system_prompt = self.prompt_builder.build_insights_system_prompt()
        user_prompt = self.prompt_builder.build_insights_user_prompt(result)

        max_attempts = 2
        
        for attempt in range(max_attempts):
            try:
                response = self.groq_client.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    model=model,
                    response_format={"type": "json_object"} # We might need to adjust prompt to return a wrapped object if API strictness requires
                )
                
                # Due to JSON mode restrictions in some APIs, if it returns an array we might need to parse it. 
                # Let's assume the prompt requests an object with an "insights" key containing the array for safety.
                # I'll update the prompt in prompt_builder if necessary, but validator expects a list directly or extracts it.
                # Actually, my prompt builder said "Return a JSON array". Some APIs don't like arrays as root in JSON mode. 
                # For safety, I'll pass it to validator.
                
                content = response.content
                # If Groq wraps it automatically, we handle it.
                if content.strip().startswith('{') and '"insights"' in content:
                    import json
                    parsed = json.loads(content)
                    if 'insights' in parsed:
                        content = json.dumps(parsed['insights'])

                validation = validate_insights_json(content)

                if validation.is_valid:
                    self.persistence.log_generation(
                        context_type="INSIGHTS",
                        stock_id=result.stock_id,
                        model_id=model,
                        status="SUCCESS",
                        prompt_version=PROMPT_VERSION,
                        latency_ms=response.latency_ms,
                        input_token_count=response.prompt_tokens,
                        output_token_count=response.completion_tokens
                    )
                    
                    insights_data = validation.data.get("insights", [])
                    self.persistence.save_insights(
                        stock_id=result.stock_id,
                        insights_data=insights_data,
                        model_id=model
                    )
                    
                    return insights_data
                else:
                    logger.warning(f"[INSIGHTS_GEN] Validation failed (Attempt {attempt+1}): {validation.error}")
            
            except Exception as e:
                logger.error(f"[INSIGHTS_GEN] Generation error (Attempt {attempt+1}): {e}")

        logger.warning(f"[INSIGHTS_GEN] Exhausted retries for {result.ticker}, activating fallback")
        fallback_insights = build_insights_fallback(result)
        
        self.persistence.log_generation(
            context_type="INSIGHTS",
            stock_id=result.stock_id,
            model_id="fallback",
            status="FALLBACK",
            prompt_version=PROMPT_VERSION
        )
        
        self.persistence.save_insights(
            stock_id=result.stock_id,
            insights_data=fallback_insights,
            model_id="fallback"
        )

        return fallback_insights
