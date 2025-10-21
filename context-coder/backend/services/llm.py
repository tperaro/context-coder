"""
LLM Service - OpenRouter Integration
Gemini 2.5 Pro via OpenRouter API
"""
import os
import httpx
import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Message(BaseModel):
    """Chat message"""
    role: str  # "user", "assistant", "system"
    content: str


class LLMResponse(BaseModel):
    """LLM API response"""
    id: str
    choices: List[Dict[str, Any]]
    model: str
    usage: Optional[Dict[str, int]] = None


class LLMService:
    """
    OpenRouter LLM Service
    
    Supports:
    - Gemini 2.5 Pro (primary model)
    - Gemini 2.0 Flash (fallback, free tier)
    - Streaming responses (optional)
    - JSON mode
    - Multi-turn conversations
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = os.getenv("DEFAULT_MODEL", "google/gemini-2.5-pro")
        
        # HTTP client with timeout
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0, connect=10.0)
        )
        
        logger.info(f"LLMService initialized with model: {self.default_model}")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        response_format: Optional[Dict[str, str]] = None,
        stream: bool = False
    ) -> LLMResponse:
        """
        Create chat completion using OpenRouter API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (defaults to gemini-2.5-pro)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            response_format: Optional {"type": "json_object"} for JSON mode
            stream: Enable streaming (not implemented in V1)
        
        Returns:
            LLMResponse with choices, model, usage
        
        Example:
            ```python
            response = await llm.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "Hello!"}
                ]
            )
            content = response.choices[0]["message"]["content"]
            ```
        """
        model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://context2task.local",  # Optional
            "X-Title": "Context2Task"  # Optional
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        # Add JSON mode if requested
        if response_format:
            payload["response_format"] = response_format
        
        try:
            logger.debug(f"Sending request to {model} with {len(messages)} messages")
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"LLM response received: {data.get('model')} - {data.get('usage')}")
            
            return LLMResponse(**data)
        
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from OpenRouter: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"LLM request failed: {str(e)}")
            raise
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
        logger.info("LLMService client closed")


# Global instance (optional pattern)
_llm_service = None

def get_llm_service() -> LLMService:
    """Get or create LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


