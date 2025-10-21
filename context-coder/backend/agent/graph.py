"""
LangGraph Agent Construction
Based on LangGraph 0.6.0 StateGraph + checkpointing
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import logging

from .state import AgentState
from .nodes.core import (
    analyze_feature_node,
    search_codebase_node,
    llm_response_node,
    update_spec_node,
    check_completion_node,
    wait_user_input_node,
)
from .nodes.optional import (
    tech_debt_node,
    security_check_node,
    generate_diagram_node,
    detect_multi_spec_node,
)
from .edges import route_user_command, should_loop_or_finish

logger = logging.getLogger(__name__)


def create_agent_graph():
    """
    Create and compile LangGraph StateGraph for Context2Task agent.
    
    Based on LangGraph 0.6.0 patterns:
    - StateGraph with TypedDict state
    - MemorySaver for checkpointing
    - Conditional edges for routing
    - Interrupt points for human-in-the-loop
    """
    
    # Initialize builder
    builder = StateGraph(AgentState)
    
    # ===== ADD CORE NODES =====
    builder.add_node("analyze", analyze_feature_node)
    builder.add_node("search", search_codebase_node)
    builder.add_node("llm_response", llm_response_node)
    builder.add_node("update_spec", update_spec_node)
    builder.add_node("check_completion", check_completion_node)
    builder.add_node("wait_input", wait_user_input_node)
    
    # ===== ADD OPTIONAL NODES =====
    builder.add_node("tech_debt", tech_debt_node)
    builder.add_node("security", security_check_node)
    builder.add_node("diagram", generate_diagram_node)
    builder.add_node("multi_spec", detect_multi_spec_node)
    
    # ===== DEFINE CORE FLOW (LINEAR) =====
    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", "search")
    builder.add_edge("search", "llm_response")
    builder.add_edge("llm_response", "update_spec")
    builder.add_edge("update_spec", "check_completion")
    
    # ===== CONDITIONAL EDGE: Should loop or finish? =====
    builder.add_conditional_edges(
        "check_completion",
        should_loop_or_finish,
        {
            "wait_input": "wait_input",
            "__end__": END
        }
    )
    
    # ===== CONDITIONAL EDGE: User command routing =====
    builder.add_conditional_edges(
        "wait_input",
        route_user_command,
        {
            "analyze": "analyze",  # Continue conversation
            "tech_debt": "tech_debt",
            "security": "security",
            "diagram": "diagram",
            "multi_spec": "multi_spec",
            "preview": "wait_input",  # Stay in wait, show preview
            "export": END,
            "__end__": END,
        }
    )
    
    # ===== OPTIONAL NODES → BACK TO MAIN LOOP =====
    builder.add_edge("tech_debt", "wait_input")
    builder.add_edge("security", "wait_input")
    builder.add_edge("diagram", "wait_input")
    builder.add_edge("multi_spec", "wait_input")
    
    # ===== COMPILE WITH CHECKPOINTING =====
    memory = MemorySaver()
    
    graph = builder.compile(
        checkpointer=memory,
        interrupt_before=["wait_input"],  # Pause before user input
    )
    
    logger.info("LangGraph agent compiled successfully")
    
    return graph


# Global graph instance
agent_graph = create_agent_graph()


