"""
Tests for Agent State Definition
"""
import pytest
from agent.state import AgentState, UserCommand, StateUpdate


def test_agent_state_structure():
    """Validate AgentState has all required fields"""
    state: AgentState = {
        "session_id": "test-123",
        "user_profile": "technical",
        "selected_repositories": ["/path/to/repo"],
        "codebase_context": [],
        "messages": [],
        "feature_summary": "Test feature",
        "spec_sections": {},
        "completion_percentage": 0,
        "is_multi_spec": False,
        "affected_repositories": [],
        "should_analyze_tech_debt": False,
        "should_check_security": False,
        "should_generate_diagram": False,
        "iteration_count": 0,
    }
    
    assert state["session_id"] == "test-123"
    assert state["user_profile"] in ["technical", "non_technical"]
    assert isinstance(state["spec_sections"], dict)
    assert state["completion_percentage"] == 0


def test_user_command_enum():
    """Validate all UserCommand values"""
    assert UserCommand.CONTINUE == "continue"
    assert UserCommand.ANALYZE_TECH_DEBT == "analyze_tech_debt"
    assert UserCommand.CHECK_SECURITY == "check_security"
    assert UserCommand.GENERATE_DIAGRAM == "generate_diagram"
    assert UserCommand.DETECT_MULTI_SPEC == "detect_multi_spec"
    assert UserCommand.PREVIEW_SPEC == "preview_spec"
    assert UserCommand.EXPORT == "export"
    assert UserCommand.CANCEL == "cancel"
    
    # Test enum has 8 commands
    assert len(UserCommand) == 8


def test_state_update_partial():
    """Test StateUpdate accepts partial state"""
    update: StateUpdate = {
        "completion_percentage": 50,
        "feature_summary": "Updated summary"
    }
    
    assert update["completion_percentage"] == 50
    assert "session_id" not in update  # Optional field


