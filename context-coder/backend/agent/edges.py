"""
Edge Routing Logic - UserCommand & Conditional Edges
Based on LangGraph 0.6.0 conditional_edges pattern
"""
from typing import Literal
import logging
from .state import AgentState, UserCommand

logger = logging.getLogger(__name__)


def route_user_command(
    state: AgentState
) -> Literal[
    "analyze",
    "tech_debt",
    "security",
    "diagram",
    "multi_spec",
    "preview",
    "export",
    "__end__"
]:
    """
    Conditional routing based on user command or AI decision.
    
    Based on LangGraph pattern:
    - Returns string matching node name or "__end__"
    - Used in graph.add_conditional_edges()
    """
    
    command = state.get("last_user_command")
    completion = state["completion_percentage"]
    session_id = state["session_id"]
    
    # Explicit user commands
    if command == UserCommand.ANALYZE_TECH_DEBT:
        logger.info(f"[{session_id}] Routing to tech_debt (user command)")
        return "tech_debt"
    
    elif command == UserCommand.CHECK_SECURITY:
        logger.info(f"[{session_id}] Routing to security (user command)")
        return "security"
    
    elif command == UserCommand.GENERATE_DIAGRAM:
        logger.info(f"[{session_id}] Routing to diagram (user command)")
        return "diagram"
    
    elif command == UserCommand.DETECT_MULTI_SPEC:
        logger.info(f"[{session_id}] Routing to multi_spec (user command)")
        return "multi_spec"
    
    elif command == UserCommand.PREVIEW_SPEC:
        logger.info(f"[{session_id}] Routing to preview")
        return "preview"
    
    elif command == UserCommand.EXPORT:
        logger.info(f"[{session_id}] Routing to export (END)")
        return "export"
    
    elif command == UserCommand.CANCEL:
        logger.info(f"[{session_id}] Routing to END (cancel)")
        return "__end__"
    
    # AI-driven decision
    if completion >= 80:
        # Spec is complete, ready for optional features or export
        logger.info(f"[{session_id}] Spec {completion}% complete, waiting for user decision")
        return "preview"  # Show preview, wait for export
    
    else:
        # Continue conversation loop
        logger.info(f"[{session_id}] Spec {completion}% complete, continuing conversation")
        return "analyze"


def should_loop_or_finish(state: AgentState) -> Literal["wait_input", "__end__"]:
    """
    Decide if should continue loop or finish.
    
    Used after update_spec node.
    """
    completion = state["completion_percentage"]
    max_iterations = 20  # Safety limit
    session_id = state["session_id"]
    
    if state.get("iteration_count", 0) >= max_iterations:
        logger.warning(f"[{session_id}] Max iterations reached, ending")
        return "__end__"
    
    if completion >= 100:
        logger.info(f"[{session_id}] Spec 100% complete, ending")
        return "__end__"
    
    return "wait_input"


