"""
Export API Endpoints
"""
from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
from typing import Dict, Optional

from services.export import get_exporter
from agent.checkpointing import get_session_manager

router = APIRouter(prefix="/api/export", tags=["export"])


class ExportRequest(BaseModel):
    session_id: str
    feature_title: Optional[str] = "Nova Feature"
    format: str = "markdown"  # "markdown" or "json"


@router.post("/spec")
async def export_spec(request: ExportRequest):
    """
    Export specification to Markdown or JSON.
    
    Args:
        session_id: Session identifier
        feature_title: Title for the spec
        format: "markdown" or "json"
    
    Returns:
        Formatted spec in requested format
    """
    session_manager = get_session_manager()
    exporter = get_exporter()
    
    # Get session state
    state = await session_manager.get_session_state(request.session_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {request.session_id} not found"
        )
    
    spec_sections = state.get("spec_sections", {})
    
    # Validate
    validation = exporter.validate(spec_sections)
    
    if not validation.is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Spec não está completo o suficiente para export",
                "validation": validation.dict()
            }
        )
    
    # Export based on format
    if request.format == "markdown":
        markdown = exporter.export_to_markdown(
            spec_sections=spec_sections,
            feature_title=request.feature_title,
            metadata={
                "session_id": request.session_id,
                "user_profile": state.get("user_profile"),
                "completion_percentage": state.get("completion_percentage", 0)
            }
        )
        
        return Response(
            content=markdown,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f'attachment; filename="{request.feature_title.replace(" ", "_")}.md"'
            }
        )
    
    elif request.format == "json":
        json_export = exporter.export_json(
            spec_sections=spec_sections,
            metadata={
                "session_id": request.session_id,
                "user_profile": state.get("user_profile"),
                "completion_percentage": state.get("completion_percentage", 0)
            }
        )
        
        return json_export
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format: {request.format}"
        )


@router.get("/validate/{session_id}")
async def validate_spec(session_id: str):
    """
    Validate spec completeness without exporting.
    
    Returns validation status and missing sections.
    """
    session_manager = get_session_manager()
    exporter = get_exporter()
    
    state = await session_manager.get_session_state(session_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    spec_sections = state.get("spec_sections", {})
    validation = exporter.validate(spec_sections)
    
    return validation.dict()


