"""
LLM Service - Multi-Provider Support
Primary: Google Gemini (Direct API)
Fallback: OpenRouter
"""
import os
import httpx
import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from abc import ABC, abstractmethod

try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    logging.warning("google-generativeai not installed. Google provider will be unavailable.")

logger = logging.getLogger(__name__)


class Message(BaseModel):
    """Chat message"""
    role: str  # "user", "assistant", "system"
    content: str


class LLMResponse(BaseModel):
    """LLM API response (normalized)"""
    id: str
    choices: List[Dict[str, Any]]
    model: str
    usage: Optional[Dict[str, Any]] = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        response_format: Optional[Dict[str, str]] = None
    ) -> LLMResponse:
        """Create chat completion"""
        pass
    
    @abstractmethod
    async def close(self):
        """Cleanup resources"""
        pass


class GoogleGeminiProvider(LLMProvider):
    """
    Google Gemini Direct API Provider
    
    Uses official google-generativeai SDK
    Free tier: https://aistudio.google.com/apikey
    """
    
    def __init__(self, api_key: str, default_model: str = "gemini-1.5-flash"):
        if not GOOGLE_AI_AVAILABLE:
            raise ImportError("google-generativeai package not installed")
        
        self.api_key = api_key
        self.default_model = default_model
        genai.configure(api_key=api_key)
        logger.info(f"GoogleGeminiProvider initialized with model: {default_model}")
    
    def _convert_messages_to_gemini_format(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Convert standard OpenAI-style messages to Gemini format
        
        Gemini expects:
        - role: "user" or "model" (not "assistant")
        - No explicit "system" role (prepend to first user message)
        """
        gemini_messages = []
        system_prompt = None
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                system_prompt = content
            elif role == "user":
                # Prepend system prompt to first user message
                if system_prompt:
                    content = f"{system_prompt}\n\n{content}"
                    system_prompt = None
                gemini_messages.append({"role": "user", "parts": [content]})
            elif role == "assistant":
                gemini_messages.append({"role": "model", "parts": [content]})
        
        return gemini_messages
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        response_format: Optional[Dict[str, str]] = None
    ) -> LLMResponse:
        """Create chat completion using Google Gemini API"""
        model_name = model or self.default_model
        
        try:
            # Convert messages to Gemini format
            gemini_messages = self._convert_messages_to_gemini_format(messages)
            
            # Configure generation
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            # JSON mode support (if requested)
            if response_format and response_format.get("type") == "json_object":
                generation_config["response_mime_type"] = "application/json"
            
            # Create model and generate
            model_instance = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
            
            # Start chat with history
            chat = model_instance.start_chat(history=gemini_messages[:-1] if len(gemini_messages) > 1 else [])
            
            # Send last message
            last_message = gemini_messages[-1]["parts"][0]
            response = await chat.send_message_async(last_message)
            
            # Normalize response to LLMResponse format
            normalized = LLMResponse(
                id=f"gemini-{hash(response.text)}",
                model=model_name,
                choices=[{
                    "message": {
                        "role": "assistant",
                        "content": response.text
                    },
                    "finish_reason": "stop"
                }],
                usage={
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0,
                }
            )
            
            logger.info(f"Google Gemini response: {model_name} - {normalized.usage}")
            return normalized
        
        except Exception as e:
            logger.error(f"Google Gemini API error: {str(e)}")
            raise
    
    async def close(self):
        """No cleanup needed for Google API"""
        pass


class OpenRouterProvider(LLMProvider):
    """
    OpenRouter API Provider (Fallback)
    
    Supports multiple models through unified API
    """
    
    def __init__(self, api_key: str, default_model: str = "google/gemini-flash-1.5"):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = default_model
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0))
        logger.info(f"OpenRouterProvider initialized with model: {default_model}")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        response_format: Optional[Dict[str, str]] = None
    ) -> LLMResponse:
        """Create chat completion using OpenRouter API"""
        model_name = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://context2task.local",
            "X-Title": "Context2Task"
        }
        
        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format:
            payload["response_format"] = response_format
        
        try:
            logger.debug(f"OpenRouter request: {model_name} with {len(messages)} messages")
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"OpenRouter response: {data.get('model')} - {data.get('usage')}")
            return LLMResponse(**data)
        
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"OpenRouter request failed: {str(e)}")
            raise
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class LLMService:
    """
    Multi-Provider LLM Service with automatic fallback
    
    Primary: Google Gemini (direct API, free tier available)
    Fallback: OpenRouter (if Google fails or not configured)
    
    Configuration via environment variables:
    - GOOGLE_API_KEY + GOOGLE_MODEL (primary)
    - OPENROUTER_API_KEY + OPENROUTER_MODEL (fallback)
    """
    
    def __init__(self):
        self.providers: List[LLMProvider] = []
        
        # Try to initialize Google Gemini (primary)
        google_key = os.getenv("GOOGLE_API_KEY")
        google_model = os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")
        
        if google_key and GOOGLE_AI_AVAILABLE:
            try:
                self.providers.append(GoogleGeminiProvider(google_key, google_model))
                logger.info("✅ Google Gemini provider initialized (PRIMARY)")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Gemini: {e}")
        elif not google_key:
            logger.warning("GOOGLE_API_KEY not set - Google Gemini unavailable")
        
        # Try to initialize OpenRouter (fallback)
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        openrouter_model = os.getenv("OPENROUTER_MODEL", "google/gemini-flash-1.5")
        
        if openrouter_key:
            try:
                self.providers.append(OpenRouterProvider(openrouter_key, openrouter_model))
                logger.info("✅ OpenRouter provider initialized (FALLBACK)")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenRouter: {e}")
        
        # Validate at least one provider
        if not self.providers:
            raise ValueError(
                "No LLM providers available. Set GOOGLE_API_KEY or OPENROUTER_API_KEY"
            )
        
        logger.info(f"LLMService ready with {len(self.providers)} provider(s)")
    
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
        Create chat completion with automatic provider fallback
        
        Tries providers in order (Google → OpenRouter) until one succeeds
        """
        last_error = None
        
        for i, provider in enumerate(self.providers):
            provider_name = provider.__class__.__name__
            try:
                logger.debug(f"Trying provider {i+1}/{len(self.providers)}: {provider_name}")
                response = await provider.chat_completion(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format=response_format
                )
                return response
            
            except Exception as e:
                last_error = e
                logger.warning(f"{provider_name} failed: {str(e)}")
                if i < len(self.providers) - 1:
                    logger.info(f"Falling back to next provider...")
                continue
        
        # All providers failed
        logger.error(f"All {len(self.providers)} provider(s) failed")
        raise last_error or Exception("No providers available")
    
    async def close(self):
        """Close all provider resources"""
        for provider in self.providers:
            try:
                await provider.close()
            except Exception as e:
                logger.warning(f"Error closing provider: {e}")
        logger.info("LLMService closed")


# Global instance (optional pattern)
_llm_service = None

def get_llm_service() -> LLMService:
    """Get or create LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service



