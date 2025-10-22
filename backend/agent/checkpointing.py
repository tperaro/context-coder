"""
Session Management with LangGraph Checkpointing
Based on LangGraph 0.6.0 MemorySaver patterns
"""
from typing import Optional, Dict, Any
import logging
from .graph import agent_graph

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Manages agent sessions with checkpointing.
    
    Based on LangGraph MemorySaver patterns.
    """
    
    def __init__(self):
        self.graph = agent_graph
    
    async def invoke_agent(
        self,
        session_id: str,
        user_message: str,
        user_command: Optional[str] = None,
        selected_repositories: Optional[list] = None,
        user_profile: str = "technical"
    ) -> Dict[str, Any]:
        """
        Invoke agent with checkpointing.
        
        Args:
            session_id: Unique session identifier (thread_id)
            user_message: User's message content
            user_command: Optional explicit command
            selected_repositories: List of repository paths
            user_profile: User profile type (technical or non_technical)
        
        Returns:
            Updated agent state
        """
        config = {"configurable": {"thread_id": session_id}}
        
        # Build input with required initial values
        input_state = {
            "session_id": session_id,
            "user_profile": user_profile,
            "selected_repositories": selected_repositories or [],
            "codebase_context": [],
            "messages": [{"role": "user", "content": user_message}],
            "feature_summary": "",
            "spec_sections": {},
            "completion_percentage": 0,
            "is_multi_spec": False,
            "affected_repositories": [],
            "should_analyze_tech_debt": False,
            "should_check_security": False,
            "should_generate_diagram": False,
            "iteration_count": 0,
        }
        
        if user_command:
            input_state["last_user_command"] = user_command
        
        try:
            # Invoke with automatic checkpointing
            result = await self.graph.ainvoke(input_state, config)
            
            logger.info(f"[{session_id}] Agent invoked successfully")
            return result
        
        except Exception as e:
            logger.error(f"[{session_id}] Agent invocation failed: {e}")
            raise
    
    async def get_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve current session state.
        
        Args:
            session_id: Session identifier
        
        Returns:
            Current state or None if session doesn't exist
        """
        config = {"configurable": {"thread_id": session_id}}
        
        try:
            state = await self.graph.aget_state(config)
            return state.values if state else None
        except Exception as e:
            logger.error(f"[{session_id}] Failed to get state: {e}")
            return None
    
    async def resume_session(
        self,
        session_id: str,
        user_message: str
    ) -> Dict[str, Any]:
        """
        Resume existing session with new message.
        
        The graph will automatically load checkpoint and continue.
        """
        return await self.invoke_agent(session_id, user_message)
    
    async def list_session_checkpoints(self, session_id: str):
        """
        List all checkpoints for a session (for debugging).
        
        Useful for time-travel features.
        """
        config = {"configurable": {"thread_id": session_id}}
        
        checkpoints = []
        async for checkpoint in self.graph.aget_state_history(config):
            checkpoints.append({
                "checkpoint_id": checkpoint.config["configurable"].get("checkpoint_id"),
                "timestamp": checkpoint.config["configurable"].get("checkpoint_ts"),
                "node": checkpoint.values.get("current_node"),
                "completion": checkpoint.values.get("completion_percentage", 0),
            })
        
        return checkpoints


# Global instance
_session_manager = None

def get_session_manager() -> SessionManager:
    """Get or create SessionManager singleton"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager


