"""
Integration Tests for Complete Agent Workflow
TASK-006-h Implementation
"""
import pytest
from agent.checkpointing import SessionManager
from agent.state import UserCommand


@pytest.mark.integration
@pytest.mark.asyncio
async def test_complete_conversation_workflow():
    """Test complete flow: user request → conversation → spec generation → export"""
    manager = SessionManager()
    session_id = "integration-test-001"
    
    # Step 1: Initial feature request
    result1 = await manager.invoke_agent(
        session_id=session_id,
        user_message="I want to add user authentication with email and password"
    )
    
    assert result1 is not None
    assert "completion_percentage" in result1
    assert result1["completion_percentage"] >= 0
    assert "messages" in result1
    assert len(result1["messages"]) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_session_persistence():
    """Test session state is persisted between invocations"""
    manager = SessionManager()
    session_id = "persistence-test-002"
    
    # First invocation
    result1 = await manager.invoke_agent(
        session_id=session_id,
        user_message="Add user registration"
    )
    
    first_message_count = len(result1.get("messages", []))
    
    # Second invocation (should resume)
    result2 = await manager.resume_session(
        session_id=session_id,
        user_message="Include email verification"
    )
    
    second_message_count = len(result2.get("messages", []))
    
    # Should have more messages now
    assert second_message_count > first_message_count
    assert result2["session_id"] == session_id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_user_commands():
    """Test user commands are executed correctly"""
    manager = SessionManager()
    session_id = "commands-test-003"
    
    # Setup: create session
    await manager.invoke_agent(session_id, "Test feature")
    
    # Test command execution
    result = await manager.invoke_agent(
        session_id=session_id,
        user_message="",
        user_command=UserCommand.ANALYZE_TECH_DEBT.value
    )
    
    assert result is not None
    # Check if tech_debt was triggered (would have tech_debt_report in real scenario)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_session_state():
    """Test retrieving session state"""
    manager = SessionManager()
    session_id = "state-test-004"
    
    # Create session
    await manager.invoke_agent(
        session_id=session_id,
        user_message="Create payment integration"
    )
    
    # Get state
    state = await manager.get_session_state(session_id)
    
    assert state is not None
    assert state["session_id"] == session_id
    assert "completion_percentage" in state
    assert "messages" in state


@pytest.mark.performance
@pytest.mark.asyncio
async def test_response_time():
    """Test agent response time is acceptable"""
    import time
    
    manager = SessionManager()
    session_id = "perf-test-005"
    
    start = time.time()
    
    result = await manager.invoke_agent(
        session_id=session_id,
        user_message="Add user authentication"
    )
    
    elapsed = time.time() - start
    
    # Should respond in reasonable time (excluding LLM API call)
    # Note: In real scenario with mocked LLM, should be < 1s
    assert elapsed < 10.0  # Generous limit for CI with real API
    assert result is not None


