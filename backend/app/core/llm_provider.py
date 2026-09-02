import os
import json
import httpx
import logging
from openai import AsyncOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

class DualLLMProvider:
    """
    Resilient Dual-LLM Abstraction Layer
    Primary: OpenAI
    Fallback: Local Ollama
    """
    def __init__(self):
        self.openai_client = None
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            
    async def generate_response(self, system_prompt: str, user_prompt: str, privacy_level: str = "normal", require_json: bool = False) -> str:
        # Force local if privacy is restricted
        if privacy_level == "restricted":
            return await self._call_ollama(system_prompt, user_prompt, require_json)
            
        # Try OpenAI if available
        if self.openai_client:
            try:
                response = await self.openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    timeout=3.0, # Timeout 3s for failover
                    response_format={"type": "json_object"} if require_json else None
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"Cloud LLM failed: {e}. Failing over to Local LLM.")
                
        # Fallback to local Ollama
        return await self._call_ollama(system_prompt, user_prompt, require_json)
        
    async def _call_ollama(self, system_prompt: str, user_prompt: str, require_json: bool = False) -> str:
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "model": settings.OLLAMA_MODEL,
                    "system": system_prompt,
                    "prompt": user_prompt,
                    "stream": False
                }
                if require_json:
                    payload["format"] = "json"
                    
                response = await client.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json=payload, timeout=30.0)
                response.raise_for_status()
                return response.json()["response"]
            except Exception as e:
                logger.error(f"Local LLM failed: {e}")
                return "{}" if require_json else "LLM Generation Failed."

llm_provider = DualLLMProvider()
