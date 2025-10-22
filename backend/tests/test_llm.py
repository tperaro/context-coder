"""
Tests for LLM Service (OpenRouter Integration)
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from services.llm import LLMService, LLMResponse


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key_123")
    monkeypatch.setenv("DEFAULT_MODEL", "google/gemini-2.5-pro")


def test_llm_service_init(mock_env):
    """Test LLMService initialization"""
    service = LLMService()
    
    assert service.api_key == "test_key_123"
    assert service.default_model == "google/gemini-2.5-pro"
    assert service.base_url == "https://openrouter.ai/api/v1"


def test_llm_service_missing_api_key(monkeypatch):
    """Test LLMService raises error when API key missing"""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY not set"):
        LLMService()


@pytest.mark.asyncio
async def test_chat_completion_success(mock_env):
    """Test successful chat completion"""
    service = LLMService()
    
    # Mock HTTP response
    mock_response = {
        "id": "gen-123",
        "model": "google/gemini-2.5-pro",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you?"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 8,
            "total_tokens": 18
        }
    }
    
    with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = Mock()
        
        response = await service.chat_completion(
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        assert isinstance(response, LLMResponse)
        assert response.model == "google/gemini-2.5-pro"
        assert len(response.choices) == 1
        assert response.choices[0]["message"]["content"] == "Hello! How can I help you?"
    
    await service.close()


@pytest.mark.asyncio
async def test_chat_completion_with_json_mode(mock_env):
    """Test chat completion with JSON response format"""
    service = LLMService()
    
    mock_response = {
        "id": "gen-456",
        "model": "google/gemini-2.0-flash-exp:free",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": '{"result": "success"}'
                }
            }
        ]
    }
    
    with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status = Mock()
        
        response = await service.chat_completion(
            messages=[{"role": "user", "content": "Respond in JSON"}],
            response_format={"type": "json_object"}
        )
        
        # Verify JSON format was requested
        call_args = mock_post.call_args
        assert call_args[1]["json"]["response_format"] == {"type": "json_object"}
        
        assert response.choices[0]["message"]["content"] == '{"result": "success"}'
    
    await service.close()


