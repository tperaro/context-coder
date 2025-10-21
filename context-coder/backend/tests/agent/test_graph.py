"""
Tests for LangGraph Agent Construction
"""
import pytest
from agent.graph import create_agent_graph


def test_graph_compilation():
    """Validate graph compiles without errors"""
    graph = create_agent_graph()
    
    assert graph is not None
    assert hasattr(graph, "invoke")
    assert hasattr(graph, "ainvoke")
    assert hasattr(graph, "stream")
    assert hasattr(graph, "astream")


@pytest.mark.asyncio
async def test_graph_has_checkpointing():
    """Test graph has checkpointing configured"""
    graph = create_agent_graph()
    
    # Graph should have checkpointer
    assert hasattr(graph, "checkpointer")
    assert graph.checkpointer is not None


# Full execution test would require mocking LLM/MCP services
# See TASK-006-h for integration tests


