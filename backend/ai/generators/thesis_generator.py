"""
ai/generators/thesis_generator.py

AI Thesis Generator.
Generates an institutional-grade investment thesis from deterministic scoring outputs.
Handles retries, validation, fallback, and persistence.
"""

from typing import Dict, Any

from engines.models import ScoringResult
from ai.groq_client import GroqClient, ModelLiteral
from ai.prompt_builder import PromptBuilder, PROMPT_VERSION
from ai.validators.output_validator import validate_thesis_json
from ai.fallback import build_thesis_fallback
from ai.persistence import AIPersistence
from core.logging import logger

class ThesisGenerator:
    def __init__(self):
        self.groq_client = GroqClient()
        self.prompt_builder = PromptBuilder()
        self.persistence = AIPersistence()

    def generate_thesis(self, result: ScoringResult, model: ModelLiteral = "llama-3.3-70b-versatile") -> Dict[str, Any]:
        """
        Generate, validate, and persist an AI thesis.
        Uses fallback if generation or validation fails.
        """
        logger.info(f"[THESIS_GEN] Generating thesis for {result.ticker} using {model}")
        
        system_prompt = self.prompt_builder.build_thesis_system_prompt()
        user_prompt = self.prompt_builder.build_thesis_user_prompt(result)

        # Retry logic for generation and validation
        max_attempts = 2
        
        for attempt in range(max_attempts):
            try:
                # 1. Generate
                response = self.groq_client.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    model=model,
                    response_format={"type": "json_object"}
                )

                # 2. Validate
                validation = validate_thesis_json(response.content)

                if validation.is_valid:
                    # 3. Log Success
                    self.persistence.log_generation(
                        context_type="THESIS",
                        stock_id=result.stock_id,
                        model_id=model,
                        status="SUCCESS",
                        prompt_version=PROMPT_VERSION,
                        latency_ms=response.latency_ms,
                        input_token_count=response.prompt_tokens,
                        output_token_count=response.completion_tokens
                    )
                    
                    # 4. Save Thesis
                    self.persistence.save_thesis(
                        result=result,
                        thesis_data=validation.data,
                        model_id=model,
                        prompt_version=PROMPT_VERSION,
                        latency_ms=response.latency_ms,
                        input_token_count=response.prompt_tokens,
                        output_token_count=response.completion_tokens,
                        is_fallback=False
                    )
                    
                    return validation.data
                else:
                    logger.warning(f"[THESIS_GEN] Validation failed (Attempt {attempt+1}): {validation.error}")
            
            except Exception as e:
                logger.error(f"[THESIS_GEN] Generation error (Attempt {attempt+1}): {e}")

        # 5. Fallback
        logger.warning(f"[THESIS_GEN] Exhausted retries for {result.ticker}, activating fallback")
        fallback_data = build_thesis_fallback(result)
        
        self.persistence.log_generation(
            context_type="THESIS",
            stock_id=result.stock_id,
            model_id="fallback",
            status="FALLBACK",
            prompt_version=PROMPT_VERSION
        )
        
        self.persistence.save_thesis(
            result=result,
            thesis_data=fallback_data,
            model_id="fallback",
            prompt_version=PROMPT_VERSION,
            is_fallback=True
        )

        return fallback_data
