"""
Tests for Edge Routing Logic
"""
import pytest
from agent.edges import route_user_command, should_loop_or_finish
from agent.state import UserCommand


def test_route_explicit_tech_debt():
    """Test routing to tech debt on explicit command"""
    state = {
        "session_id": "test",
        "last_user_command": UserCommand.ANALYZE_TECH_DEBT,
        "completion_percentage": 50,
    }
    
    route = route_user_command(state)
    assert route == "tech_debt"


def test_route_completion_triggers_preview():
    """Test routing to preview when spec >= 80% complete"""
    state = {
        "session_id": "test",
        "completion_percentage": 85,  # >= 80%
    }
    
    route = route_user_command(state)
    assert route == "preview"


def test_route_continue_when_incomplete():
    """Test routing to continue when spec < 80%"""
    state = {
        "session_id": "test",
        "completion_percentage": 40,
    }
    
    route = route_user_command(state)
    assert route == "analyze"


def test_route_export_command():
    """Test routing to END on export command"""
    state = {
        "session_id": "test",
        "last_user_command": UserCommand.EXPORT,
        "completion_percentage": 90,
    }
    
    route = route_user_command(state)
    assert route == "export"


def test_should_loop_or_finish_continue():
    """Test should continue loop"""
    state = {
        "session_id": "test",
        "completion_percentage": 50,
        "iteration_count": 5,
    }
    
    result = should_loop_or_finish(state)
    assert result == "wait_input"


def test_should_loop_or_finish_max_iterations():
    """Test ends on max iterations"""
    state = {
        "session_id": "test",
        "completion_percentage": 50,
        "iteration_count": 25,  # > 20
    }
    
    result = should_loop_or_finish(state)
    assert result == "__end__"


def test_should_loop_or_finish_100_percent():
    """Test ends when 100% complete"""
    state = {
        "session_id": "test",
        "completion_percentage": 100,
        "iteration_count": 5,
    }
    
    result = should_loop_or_finish(state)
    assert result == "__end__"


