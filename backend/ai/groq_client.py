"""
ai/groq_client.py

Typed Groq wrapper for the NorthScale AI Layer.

Features:
- model routing
- retry support
- timeout handling
- latency tracking
- structured JSON enforcement
- request logging
"""

import json
import time
from typing import Any, Dict, Optional, Literal

from groq import Groq
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from core.config import settings
from core.logging import logger

# Recommended models
ModelLiteral = Literal["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]

class GroqResponse(BaseModel):
    content: str
    model: str
    latency_ms: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class GroqClient:
    def __init__(self):
        # We assume GROQ_API_KEY is available in settings
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: ModelLiteral = "llama-3.3-70b-versatile",
        temperature: float = 0.2,
        max_tokens: int = 1024,
        response_format: Optional[Dict[str, str]] = None
    ) -> GroqResponse:
        """
        Execute a generation request to Groq.
        Supports automatic retries and logs generation latency.
        """
        logger.info(f"[GROQ_CLIENT] Executing request with model {model}")
        
        start_time = time.time()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
                timeout=30.0 # Timeout handling
            )
        except Exception as e:
            logger.error(f"[GROQ_CLIENT] Generation failed: {str(e)}")
            raise e
            
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)
        
        choice = completion.choices[0].message.content
        usage = completion.usage
        
        prompt_tokens = getattr(usage, "prompt_tokens", 0)
        completion_tokens = getattr(usage, "completion_tokens", 0)
        total_tokens = getattr(usage, "total_tokens", 0)

        logger.info(f"[GROQ_CLIENT] Success: latency={latency_ms}ms, tokens={total_tokens}")
        
        return GroqResponse(
            content=choice or "",
            model=model,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )
