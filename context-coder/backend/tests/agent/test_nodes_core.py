"""
Tests for Core Graph Nodes
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from agent.nodes.core import (
    analyze_feature_node,
    check_completion_node,
    format_codebase_context
)
from agent.state import AgentState


@pytest.fixture
def base_state():
    """Base state for testing"""
    return {
        "session_id": "test",
        "user_profile": "technical",
        "selected_repositories": ["/repo1"],
        "messages": [{"role": "user", "content": "Add user authentication"}],
        "feature_summary": "",
        "spec_sections": {},
        "completion_percentage": 0,
        "is_multi_spec": False,
        "affected_repositories": [],
        "should_analyze_tech_debt": False,
        "should_check_security": False,
        "should_generate_diagram": False,
        "iteration_count": 0,
        "codebase_context": [],
    }


@pytest.mark.asyncio
async def test_analyze_feature_node(base_state):
    """Test feature analysis node"""
    with patch("agent.nodes.core.get_llm_service") as mock_llm:
        mock_service = Mock()
        mock_service.chat_completion = AsyncMock(return_value=Mock(
            choices=[{
                "message": {
                    "content": '{"main_goal": "Add authentication", "complexity": 4, "questions": ["Q1", "Q2", "Q3"]}'
                }
            }]
        ))
        mock_llm.return_value = mock_service
        
        result = await analyze_feature_node(base_state)
        
        assert "feature_summary" in result
        assert result["feature_summary"] == "Add authentication"
        assert result.get("feature_complexity") == 4
        assert "messages" in result


@pytest.mark.asyncio
async def test_check_completion_node():
    """Test completion percentage calculation"""
    state = {
        "spec_sections": {
            "descricao": "Test description with more than 20 chars here",
            "user_story": "As a user, I want to authenticate...",
            # 2 of 10 filled
        },
        "completion_percentage": 0,
    }
    
    result = await check_completion_node(state)
    
    assert result["completion_percentage"] == 20  # 2/10 = 20%


def test_format_codebase_context():
    """Test context formatting"""
    results = [
        {"file": "auth.py", "line": 42, "content": "def authenticate():"},
        {"file": "models.py", "line": 15, "content": "class User:"}
    ]
    
    formatted = format_codebase_context(results)
    
    assert "auth.py:42" in formatted
    assert "def authenticate():" in formatted
    assert "models.py:15" in formatted


