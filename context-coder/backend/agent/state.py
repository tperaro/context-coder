"""
Agent State - LangGraph TypedDict State Definition
Based on LangGraph 0.6.0 patterns
"""
from typing import Annotated, List, Dict, Optional, Literal
from typing_extensions import TypedDict, NotRequired
from operator import add
from enum import Enum

from langgraph.graph.message import add_messages


class UserCommand(str, Enum):
    """User-triggered commands for explicit graph control"""
    CONTINUE = "continue"  # Continue conversation
    ANALYZE_TECH_DEBT = "analyze_tech_debt"  # Trigger tech debt analysis
    CHECK_SECURITY = "check_security"  # Trigger security check
    GENERATE_DIAGRAM = "generate_diagram"  # Generate Mermaid diagram
    DETECT_MULTI_SPEC = "detect_multi_spec"  # Detect multi-repo split
    PREVIEW_SPEC = "preview_spec"  # Preview generated spec
    EXPORT = "export"  # Export final spec
    CANCEL = "cancel"  # Cancel current operation


class AgentState(TypedDict):
    """
    Complete state schema for Context2Task agent.
    
    Based on LangGraph 0.6.0 StateGraph patterns:
    - Uses TypedDict for structured state
    - Annotated reducers for list aggregation
    - NotRequired for optional fields
    """
    
    # ===== SESSION INFO =====
    session_id: str  # Unique session identifier
    user_profile: Literal["technical", "non_technical"]  # User profile type
    
    # ===== REPOSITORIES =====
    selected_repositories: List[str]  # List of repository paths
    codebase_context: List[Dict]  # MCP search results (relevant code snippets)
    
    # ===== CONVERSATION =====
    # Using add_messages reducer from langgraph.graph.message
    messages: Annotated[List[Dict[str, str]], add_messages]  # Chat history
    
    # ===== FEATURE ANALYSIS =====
    feature_summary: str  # Extracted feature description
    feature_complexity: NotRequired[int]  # Complexity score (1-5)
    
    # ===== SPEC GENERATION =====
    spec_sections: Dict[str, str]  # 10 sections from company-task-template.md
    completion_percentage: int  # 0-100 (threshold: 80%)
    
    # ===== OPTIONAL FEATURES =====
    tech_debt_report: NotRequired[Dict]  # AI-powered tech debt analysis
    security_report: NotRequired[Dict]  # LGPD + OWASP + Company rules
    mermaid_diagram: NotRequired[str]  # Generated Mermaid code
    
    # ===== MULTI-SPEC =====
    is_multi_spec: bool  # Whether to split into multiple specs
    affected_repositories: List[str]  # Repos impacted by feature
    multi_spec_details: NotRequired[Dict]  # Split details per repo
    
    # ===== CONTROL FLAGS =====
    should_analyze_tech_debt: bool  # User requested tech debt check
    should_check_security: bool  # User requested security check
    should_generate_diagram: bool  # User requested diagram
    
    # ===== USER COMMANDS =====
    last_user_command: NotRequired[UserCommand]  # Last explicit command
    
    # ===== METADATA =====
    iteration_count: Annotated[int, add]  # Number of conversation turns
    current_node: NotRequired[str]  # Current graph node (for debugging)


# Helper type for node return values
class StateUpdate(TypedDict, total=False):
    """Partial state update (any subset of AgentState fields)"""
    session_id: str
    user_profile: Literal["technical", "non_technical"]
    selected_repositories: List[str]
    codebase_context: List[Dict]
    messages: List[Dict[str, str]]
    feature_summary: str
    feature_complexity: int
    spec_sections: Dict[str, str]
    completion_percentage: int
    tech_debt_report: Dict
    security_report: Dict
    mermaid_diagram: str
    is_multi_spec: bool
    affected_repositories: List[str]
    multi_spec_details: Dict
    should_analyze_tech_debt: bool
    should_check_security: bool
    should_generate_diagram: bool
    last_user_command: UserCommand
    iteration_count: int
    current_node: str


