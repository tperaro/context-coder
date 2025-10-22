"""
Agent API Endpoints - FastAPI Integration
Based on FastAPI 0.116.1 async patterns
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from agent.checkpointing import get_session_manager
from agent.state import UserCommand

router = APIRouter(prefix="/api", tags=["agent"])


# ===== REQUEST/RESPONSE MODELS =====

class ChatRequest(BaseModel):
    session_id: str
    message: str
    command: Optional[UserCommand] = None
    selected_repositories: Optional[List[str]] = None
    user_profile: str = "technical"


class ChatResponse(BaseModel):
    session_id: str
    ai_response: str
    completion_percentage: int
    spec_sections: Dict[str, str]
    is_complete: bool


class SessionStateResponse(BaseModel):
    session_id: str
    user_profile: str
    selected_repositories: List[str]
    completion_percentage: int
    current_node: Optional[str]
    iteration_count: int


# ===== ENDPOINTS =====

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - send message to agent.
    
    Automatically resumes session if exists, creates new if doesn't.
    """
    session_manager = get_session_manager()
    
    try:
        result = await session_manager.invoke_agent(
            session_id=request.session_id,
            user_message=request.message,
            user_command=request.command.value if request.command else None,
            selected_repositories=request.selected_repositories,
            user_profile=request.user_profile
        )
        
        # Extract AI response
        messages = result.get("messages", [])
        ai_messages = []
        for m in messages:
            # Handle both dict and LangChain message objects
            if hasattr(m, 'type'):
                # LangChain message object
                if m.type == "ai":
                    ai_messages.append(m)
            elif isinstance(m, dict) and m.get("role") == "assistant":
                ai_messages.append(m)
        
        if ai_messages:
            last_ai = ai_messages[-1]
            ai_response = last_ai.content if hasattr(last_ai, 'content') else last_ai.get("content", "")
        else:
            ai_response = ""
        
        return ChatResponse(
            session_id=result["session_id"],
            ai_response=ai_response,
            completion_percentage=result.get("completion_percentage", 0),
            spec_sections=result.get("spec_sections", {}),
            is_complete=result.get("completion_percentage", 0) >= 80
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent invocation failed: {str(e)}"
        )


@router.post("/command/{session_id}/{command}")
async def execute_command(session_id: str, command: UserCommand):
    """
    Execute explicit user command.
    
    Examples:
    - POST /api/command/session-123/analyze_tech_debt
    - POST /api/command/session-123/export
    """
    session_manager = get_session_manager()
    
    try:
        result = await session_manager.invoke_agent(
            session_id=session_id,
            user_message="",  # Empty message for commands
            user_command=command.value
        )
        
        return {"status": "success", "result": result}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Command execution failed: {str(e)}"
        )


@router.get("/session/{session_id}/state", response_model=SessionStateResponse)
async def get_session_state(session_id: str):
    """
    Get current session state.
    
    Useful for debugging and displaying current progress in UI.
    """
    session_manager = get_session_manager()
    
    state = await session_manager.get_session_state(session_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    return SessionStateResponse(
        session_id=state["session_id"],
        user_profile=state["user_profile"],
        selected_repositories=state["selected_repositories"],
        completion_percentage=state.get("completion_percentage", 0),
        current_node=state.get("current_node"),
        iteration_count=state.get("iteration_count", 0)
    )


@router.get("/session/{session_id}/checkpoints")
async def list_checkpoints(session_id: str):
    """
    List all checkpoints for session (debugging).
    
    Useful for implementing time-travel features.
    """
    session_manager = get_session_manager()
    
    checkpoints = await session_manager.list_session_checkpoints(session_id)
    
    return {"session_id": session_id, "checkpoints": checkpoints}

