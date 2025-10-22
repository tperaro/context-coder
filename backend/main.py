"""
Context2Task Backend - FastAPI Application
AI-Powered Feature Specification Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Context2Task API",
    description="AI-Powered Feature Specification Platform using LangGraph + Gemini 2.5 Pro",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Returns API status and environment info
    """
    # Determine active LLM provider
    llm_provider = "None"
    if os.getenv("GOOGLE_API_KEY"):
        llm_provider = f"Google Gemini ({os.getenv('GOOGLE_MODEL', 'gemini-1.5-flash')})"
        if os.getenv("OPENROUTER_API_KEY"):
            llm_provider += " + OpenRouter (fallback)"
    elif os.getenv("OPENROUTER_API_KEY"):
        llm_provider = f"OpenRouter ({os.getenv('OPENROUTER_MODEL', 'gemini-flash-1.5')})"
    
    return {
        "status": "healthy",
        "service": "context2task-backend",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "llm_provider": llm_provider,
        "mcp_status": "connected"
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "Context2Task API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

# API Info endpoint
@app.get("/api/info", tags=["Info"])
async def api_info():
    """
    API configuration and capabilities
    """
    return {
        "features": [
            "Multi-turn conversations with AI",
            "Codebase context via MCP",
            "LangGraph agent orchestration",
            "Multi-repository analysis",
            "Tech debt detection (AI-powered)",
            "Security checklist (LGPD + OWASP)",
            "Mermaid diagram generation",
            "Markdown export (company template)"
        ],
        "llm_providers": {
            "primary": {
                "name": "Google Gemini (Direct API)",
                "model": os.getenv("GOOGLE_MODEL", "gemini-2.0-flash-exp"),
                "enabled": bool(os.getenv("GOOGLE_API_KEY"))
            },
            "fallback": {
                "name": "OpenRouter",
                "model": os.getenv("OPENROUTER_MODEL", "google/gemini-flash-1.5"),
                "enabled": bool(os.getenv("OPENROUTER_API_KEY"))
            }
        },
        "mcp": {
            "provider": "zilliztech/claude-context",
            "features": ["index_codebase", "search_code", "clear_index", "get_indexing_status"]
        }
    }

# Include API routers
from api.agent import router as agent_router
from api.export import router as export_router
from api.github import router as github_router
from api.repositories import router as repositories_router

app.include_router(agent_router)
app.include_router(export_router)
app.include_router(github_router)
app.include_router(repositories_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

