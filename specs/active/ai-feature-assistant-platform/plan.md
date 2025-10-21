# Context2Task - Technical Implementation Plan

**Feature ID**: ai-feature-assistant-platform  
**Platform Name**: Context2Task  
**Tagline**: "From codebase context to actionable tasks"

---

## 📋 Executive Summary

### Overview
Context2Task é uma plataforma AI-powered que transforma ideias vagas de features em especificações técnicas detalhadas. Utiliza contexto de repositórios (via MCP) e LLM (Gemini 2.5 Pro) para gerar documentação acionável no formato da empresa, com suporte a multi-repositórios, perfis adaptativos, e análises inteligentes de tech debt e segurança.

### Key Goals
1. Reduzir tempo de especificação de 2-3h para < 10 minutos
2. Suportar 50 features/mês com qualidade consistente
3. Adaptar-se a usuários técnicos e não-técnicos
4. Gerar specs no formato padronizado da empresa
5. Integrar com GitHub Projects para gestão de backlog

### Success Criteria
- ✅ Setup completo em < 2 minutos (`docker-compose up`)
- ✅ Tempo de resposta < 3s para busca de contexto
- ✅ 95% das specs incluem todos campos obrigatórios
- ✅ NPS > 8/10 dos usuários
- ✅ Taxa de uso: 80% das features passam pela plataforma

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│                     (React + TypeScript)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/WebSocket
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                    │
│                                                               │
│  ┌────────────────┐         ┌──────────────────────┐        │
│  │  Frontend      │         │  Backend API         │        │
│  │  Container     │◄───────►│  Container           │        │
│  │  (Nginx+React) │  HTTP   │  (FastAPI+Python)    │        │
│  │  Port: 3000    │         │  Port: 8000          │        │
│  └────────────────┘         └──────────┬───────────┘        │
│                                         │                     │
│                                         │                     │
│                            ┌────────────▼───────────┐        │
│                            │  MCP Client            │        │
│                            │  (Subprocess/Stdio)    │        │
│                            └────────────┬───────────┘        │
└─────────────────────────────────────────┼───────────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ↓                     ↓                     ↓
          ┌──────────────────┐  ┌────────────────┐  ┌─────────────────┐
          │ OpenRouter API   │  │ MCP Server     │  │ Zilliz Cloud    │
          │ (Gemini 2.5 Pro) │  │ (claude-context)│  │ (Milvus)        │
          │ External         │  │ npx subprocess  │  │ External        │
          └──────────────────┘  └────────┬───────┘  └─────────────────┘
                                         │
                                         ↓
                                ┌─────────────────┐
                                │ OpenAI API      │
                                │ (Embeddings)    │
                                │ External        │
                                └─────────────────┘
```

### Component Breakdown

#### 1. Frontend Container
- **Tech**: React 18+, TypeScript, Vite
- **UI Library**: shadcn/ui (Radix UI + Tailwind CSS)
- **State**: React Query + Zustand
- **WebSocket**: Socket.io-client (real-time updates)
- **Build**: Vite → Static files → Nginx
- **Port**: 3000 (external)

#### 2. Backend Container
- **Tech**: Python 3.10+, FastAPI
- **Agent Framework**: **LangGraph** (stateful workflows, checkpointing, human-in-the-loop)
- **ASGI Server**: Uvicorn
- **Async**: asyncio + aiohttp
- **MCP Integration**: Python subprocess + JSON-RPC
- **Session Storage**: LangGraph MemorySaver (in-memory checkpointing V1)
- **Port**: 8000 (internal)

#### 3. External Services
- **OpenRouter**: LLM API (Gemini 2.5 Pro)
- **MCP Server**: claude-context via npx
- **Zilliz Cloud**: Vector database (Milvus Serverless)
- **OpenAI**: Embeddings API (text-embedding-3-small)

---

## 💻 Technology Stack

### Frontend Stack

| Category | Technology | Justification |
|----------|-----------|---------------|
| **Framework** | React 18 + TypeScript | Type safety, component reusability, large ecosystem |
| **Build Tool** | Vite | Fast HMR, modern ESM, optimal bundling |
| **UI Library** | shadcn/ui | Copy-paste components, full customization, Radix primitives, accessibility |
| **Styling** | Tailwind CSS | Utility-first, consistent design system, small bundle |
| **State Management** | Zustand | Lightweight, simple API, no boilerplate |
| **Data Fetching** | React Query | Caching, optimistic updates, automatic refetch |
| **WebSocket** | Socket.io-client | Real-time updates, auto-reconnect, fallback |
| **Routing** | React Router v6 | Standard, declarative routing |
| **Forms** | React Hook Form | Performance, minimal re-renders, validation |
| **Validation** | Zod | TypeScript-first, runtime validation |
| **Markdown** | react-markdown + remark | Render MD preview, syntax highlighting |
| **Diagrams** | Mermaid | Render architecture diagrams |
| **Voice** | Web Speech API | Browser native, no external deps (fallback: Whisper API) |

### Backend Stack

| Category | Technology | Justification |
|----------|-----------|---------------|
| **Framework** | FastAPI | Async, auto OpenAPI docs, type hints, fast |
| **Agent Orchestration** | **LangGraph** | **Stateful workflows, multi-turn conversations, human-in-the-loop, checkpointing** |
| **LLM Framework** | LangChain | Prompt templates, memory abstractions, tool calling |
| **ASGI Server** | Uvicorn | Production-grade, async, WebSocket support |
| **HTTP Client** | httpx | Async HTTP, retry logic, timeouts |
| **MCP Client** | Custom (subprocess) | Stdio communication with Node.js MCP |
| **Session Storage** | MemorySaver (LangGraph) → PostgresSaver (V2) | In-memory checkpointing for V1, persistent for V2 |
| **Validation** | Pydantic v2 | FastAPI native, type safety, serialization |
| **Logging** | structlog | Structured logs, JSON output |
| **Config** | pydantic-settings | Type-safe env vars |
| **Testing** | pytest + pytest-asyncio | Async testing, fixtures, parametrization |

### Infrastructure

| Category | Technology | Justification |
|----------|-----------|---------------|
| **Containerization** | Docker + Docker Compose | Reproducible, isolated, simple deployment |
| **Web Server** | Nginx | Serve React static files, reverse proxy |
| **OS** | Ubuntu 22.04 | Target deployment environment |
| **Environment** | .env file | Simple config management |

---

## 🗄️ Data Models

### Session Storage (In-Memory)

```python
# backend/models/session.py

from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class UserProfile(str, Enum):
    TECHNICAL = "technical"
    NON_TECHNICAL = "non_technical"

class ConversationMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: datetime
    metadata: Optional[Dict] = None

class RepositoryInfo(BaseModel):
    name: str
    path: str
    indexed: bool
    last_indexed: Optional[datetime] = None

class SpecProgress(BaseModel):
    """Progress for single spec (used in multi-spec)"""
    repository: str
    completion_percentage: int  # 0-100
    sections_completed: List[str]
    last_updated: datetime

class SpecDocument(BaseModel):
    """Generated specification document"""
    title: str
    description: str
    user_story: str
    expected_results: List[str]
    technical_details: List[str]
    checklist: List[str]
    acceptance_criteria: List[str]
    definition_of_done: List[str]
    observations: Optional[str] = None
    references: Optional[List[str]] = None
    risks: Optional[List[str]] = None
    tech_debt_analysis: Optional[Dict] = None
    security_analysis: Optional[Dict] = None
    mermaid_diagram: Optional[str] = None

class Session(BaseModel):
    """Main session object (in-memory)"""
    session_id: str
    user_profile: UserProfile
    selected_repositories: List[RepositoryInfo]
    conversation_history: List[ConversationMessage]
    specs: Dict[str, SpecDocument]  # repo_name -> spec
    multi_spec_mode: bool
    spec_progress: List[SpecProgress]  # if multi-spec
    created_at: datetime
    last_activity: datetime
    
# Global in-memory storage
sessions: Dict[str, Session] = {}
```

### API Request/Response Models

```python
# backend/models/api.py

class CreateSessionRequest(BaseModel):
    user_profile: UserProfile
    selected_repositories: List[str]  # repo paths

class CreateSessionResponse(BaseModel):
    session_id: str
    repositories: List[RepositoryInfo]

class SendMessageRequest(BaseModel):
    session_id: str
    message: str
    voice_input: Optional[bool] = False

class SendMessageResponse(BaseModel):
    message_id: str
    assistant_reply: str
    context_used: List[Dict]  # MCP search results
    spec_updates: Optional[Dict] = None
    multi_spec_detected: Optional[bool] = None
    affected_repositories: Optional[List[str]] = None

class AnalyzeTechDebtRequest(BaseModel):
    session_id: str
    repository: Optional[str] = None  # If None, analyze all

class TechDebtItem(BaseModel):
    severity: str  # "critical" | "medium" | "low"
    category: str  # "code_smell" | "performance" | etc.
    file: str
    line: int
    issue: str
    suggestion: str
    effort_hours: float

class AnalyzeTechDebtResponse(BaseModel):
    total_items: int
    critical: List[TechDebtItem]
    medium: List[TechDebtItem]
    low: List[TechDebtItem]
    total_effort_hours: float

class GenerateDiagramRequest(BaseModel):
    session_id: str
    diagram_type: str  # "architecture" | "flow" | "sequence" | "er"
    repository: Optional[str] = None

class GenerateDiagramResponse(BaseModel):
    mermaid_code: str
    preview_url: Optional[str] = None

class ExportSpecRequest(BaseModel):
    session_id: str
    format: str  # "markdown" | "json" | "yaml"
    repositories: Optional[List[str]] = None  # If None, export all

class ExportSpecResponse(BaseModel):
    specs: Dict[str, str]  # repo_name -> formatted_content
    download_urls: Optional[Dict[str, str]] = None
```

---

## 🤖 LangGraph Agent Architecture

### Overview

O **Context2Task** utiliza **LangGraph** para orquestração do agente conversacional. A arquitetura é **híbrida**, onde o estado do grafo é controlado tanto pela **IA** (decisões automáticas) quanto pelo **usuário** (comandos explícitos).

**Documento Detalhado**: Ver [`langgraph-architecture.md`](./langgraph-architecture.md) para implementação completa.

### Princípios de Design

1. **Modularidade**: Cada funcionalidade é um nó independente no grafo
2. **User-Controllable**: Usuário pode alterar o fluxo via comandos explícitos
3. **AI-Driven**: IA decide próximos passos automaticamente quando apropriado
4. **Interruptible**: Execução pode pausar e retomar (checkpointing)
5. **Observable**: Todas transições são logadas

### Grafo Simplificado

```
START
  ↓
[Select Profile] → [Select Repos] → [Initial Input]
  ↓
[Analyze Feature] ⟷ [Search Codebase]
  ↓
[LLM Response] → [WAIT USER INPUT] ← (interrupt point)
  ↓
  ├─→ Regular message → [Analyze Feature] (loop)
  ├─→ "analyze_tech_debt" → [Tech Debt Node] → [WAIT]
  ├─→ "check_security" → [Security Node] → [WAIT]
  ├─→ "generate_diagram" → [Diagram Node] → [WAIT]
  └─→ "finish_spec" → [Prepare Export] → [Multi-Spec Detection]
                                          ↓
                                      [Export MD/GitHub] → END
```

### Estado do Grafo (AgentState)

```python
from typing import TypedDict, Annotated, Literal
from langgraph.graph import add_messages

class AgentState(TypedDict):
    # Session
    session_id: str
    user_profile: Literal["technical", "non_technical"]
    selected_repositories: list[str]
    
    # Conversation
    messages: Annotated[list[dict], add_messages]
    current_user_input: str | None
    
    # AI Analysis
    feature_summary: str | None
    codebase_context: list[dict]
    
    # Spec Building
    spec_sections: dict[str, str]
    completion_percentage: int
    
    # Optional Analysis (User-Triggered)
    tech_debt_report: dict | None
    security_report: dict | None
    mermaid_diagram: str | None
    
    # Control Flow
    current_node: str
    next_action: str | None  # IA decision
    user_command: str | None  # User override
    
    # Export
    ready_for_export: bool
    export_format: Literal["markdown", "github"] | None
```

### Nós Principais

| Nó | Tipo | Descrição |
|----|------|-----------|
| `analyze_feature` | AI-Driven | Analisa feature, decide se precisa buscar contexto |
| `search_codebase` | Tool Call | Busca código relevante via MCP |
| `llm_response` | AI-Driven | Gera resposta adaptada ao perfil do usuário |
| `wait_user_input` | Interrupt | **Pausa execução** até usuário enviar mensagem/comando |
| `tech_debt_analysis` | User-Triggered | Análise de débito técnico (AI + MCP) |
| `security_check` | User-Triggered | Verificação de segurança |
| `generate_diagram` | User-Triggered | Gera diagrama Mermaid |
| `prepare_export` | Final | Prepara spec para exportação |
| `detect_multi_spec` | AI-Driven | Detecta se precisa split multi-spec |
| `export_markdown` / `export_github` | Final | Exporta specs |

### Roteamento Condicional (User Commands)

```python
def route_user_command(state: AgentState) -> str:
    """Usuário controla o fluxo do grafo aqui"""
    
    if state["user_command"] == "analyze_tech_debt":
        return "tech_debt"  # Muda fluxo para análise opcional
    
    if state["user_command"] == "check_security":
        return "security"
    
    if state["user_command"] == "finish_spec":
        return "export"
    
    # Default: continuar conversação normal
    return "continue"
```

### Integração com FastAPI

```python
# backend/agent/graph.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

def compile_graph():
    workflow = StateGraph(AgentState)
    
    # Adicionar nós...
    workflow.add_node("analyze", analyze_feature_node)
    workflow.add_node("search", search_codebase_node)
    # ... outros nós
    
    # Adicionar edges...
    workflow.add_conditional_edges(
        "wait_user_input",
        route_user_command,
        {"continue": "analyze", "tech_debt": "tech_debt_analysis", ...}
    )
    
    # Compile com checkpointing
    memory = MemorySaver()  # V1: in-memory
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["wait_user_input"]
    )

# backend/api/session.py
from fastapi import APIRouter

app = compile_graph()

@router.post("/session/message")
async def send_message(session_id: str, message: str, command: str | None):
    config = {"configurable": {"thread_id": session_id}}
    
    # Continuar execução do grafo
    result = await app.ainvoke(
        {"current_user_input": message, "user_command": command},
        config
    )
    
    return result
```

### Checkpointing e Persistência

- **V1 (MVP)**: `MemorySaver` (in-memory)
- **V2 (Produção)**: `PostgresSaver` ou `RedisSaver`

Benefícios:
- Sessões podem ser retomadas após restart
- Histórico completo de todas transições de estado
- Rollback para estados anteriores se necessário

### Extensibilidade

Para adicionar novo nó opcional (ex: "Estimate Effort"):

1. Criar função `estimate_effort_node(state: AgentState) -> dict`
2. Adicionar ao grafo: `workflow.add_node("estimate", estimate_effort_node)`
3. Adicionar edge: `workflow.add_edge("estimate", "wait_user_input")`
4. Atualizar roteamento: `if command == "estimate": return "estimate"`

**Referência Completa**: [`langgraph-architecture.md`](./langgraph-architecture.md)

---

## 🔌 API Design

### REST API Endpoints

#### Session Management

```http
POST /api/sessions
Content-Type: application/json

{
  "user_profile": "technical",
  "selected_repositories": ["/path/to/backend", "/path/to/frontend"]
}

Response 201:
{
  "session_id": "sess_abc123",
  "repositories": [
    {
      "name": "backend-api",
      "path": "/path/to/backend",
      "indexed": true,
      "last_indexed": "2025-10-19T10:30:00Z"
    }
  ]
}
```

```http
GET /api/sessions/{session_id}

Response 200:
{
  "session_id": "sess_abc123",
  "user_profile": "technical",
  "multi_spec_mode": false,
  "conversation_history": [...],
  "last_activity": "2025-10-19T11:45:00Z"
}
```

```http
DELETE /api/sessions/{session_id}

Response 204: No Content
```

#### Conversation

```http
POST /api/conversations/message
Content-Type: application/json

{
  "session_id": "sess_abc123",
  "message": "Quero adicionar notificações push no app",
  "voice_input": false
}

Response 200:
{
  "message_id": "msg_xyz789",
  "assistant_reply": "Entendi! Detectei que isso impacta backend e frontend...",
  "context_used": [
    {
      "file": "backend/services/notification.py",
      "lines": [45, 78],
      "relevance": 0.92
    }
  ],
  "multi_spec_detected": true,
  "affected_repositories": ["backend-api", "frontend-web"]
}
```

```http
GET /api/conversations/{session_id}/history

Response 200:
{
  "messages": [
    {
      "role": "user",
      "content": "...",
      "timestamp": "2025-10-19T11:30:00Z"
    }
  ]
}
```

#### MCP Integration

```http
POST /api/mcp/search
Content-Type: application/json

{
  "repository": "/path/to/backend",
  "query": "notification system push",
  "limit": 10
}

Response 200:
{
  "results": [
    {
      "file": "backend/services/notification.py",
      "start_line": 45,
      "end_line": 78,
      "content": "class NotificationService...",
      "score": 0.92
    }
  ]
}
```

```http
POST /api/mcp/index
Content-Type: application/json

{
  "repository": "/path/to/backend",
  "force": false
}

Response 202:
{
  "status": "indexing",
  "message": "Indexing started"
}
```

```http
GET /api/mcp/index/status/{repository}

Response 200:
{
  "status": "indexing",
  "percentage": 65,
  "files_processed": 325,
  "total_files": 500
}
```

#### Analysis Features

```http
POST /api/analysis/tech-debt
Content-Type: application/json

{
  "session_id": "sess_abc123",
  "repository": "backend-api"
}

Response 200:
{
  "total_items": 8,
  "critical": [
    {
      "severity": "critical",
      "category": "code_smell",
      "file": "backend/services/notification.py",
      "line": 145,
      "issue": "Method has 85 lines (max: 20)",
      "suggestion": "Extract smaller methods",
      "effort_hours": 2.0
    }
  ],
  "total_effort_hours": 5.5
}
```

```http
POST /api/analysis/security
Content-Type: application/json

{
  "session_id": "sess_abc123"
}

Response 200:
{
  "total_checks": 9,
  "passed": 6,
  "failed": 3,
  "critical_issues": [
    {
      "category": "lgpd",
      "issue": "Handles CPF without consent mechanism",
      "recommendation": "Add explicit consent checkbox"
    }
  ]
}
```

```http
POST /api/analysis/diagram
Content-Type: application/json

{
  "session_id": "sess_abc123",
  "diagram_type": "architecture",
  "repository": "backend-api"
}

Response 200:
{
  "mermaid_code": "graph TB\n  A[Frontend]...",
  "preview_url": null
}
```

#### Export

```http
POST /api/export
Content-Type: application/json

{
  "session_id": "sess_abc123",
  "format": "markdown",
  "repositories": ["backend-api", "frontend-web"]
}

Response 200:
{
  "specs": {
    "backend-api": "# 📌 Descrição...",
    "frontend-web": "# 📌 Descrição..."
  }
}
```

```http
POST /api/export/github-project
Content-Type: application/json

{
  "session_id": "sess_abc123",
  "project_board": "backlog",
  "repositories": ["backend-api"]
}

Response 201:
{
  "cards_created": [
    {
      "repository": "backend-api",
      "card_id": "GH_card_123",
      "card_url": "https://github.com/org/repo/projects/1#card-123"
    }
  ]
}
```

### WebSocket Events

```javascript
// Client connects
ws://localhost:8000/ws/{session_id}

// Server → Client events
{
  "event": "spec_update",
  "data": {
    "repository": "backend-api",
    "section": "technical_details",
    "content": "..."
  }
}

{
  "event": "analysis_progress",
  "data": {
    "type": "tech_debt",
    "progress": 65,
    "message": "Analyzing code smells..."
  }
}

{
  "event": "multi_spec_detected",
  "data": {
    "repositories": ["backend-api", "frontend-web", "mobile-app"],
    "auto_split": true
  }
}
```

---

## 🔐 Security Implementation

### 1. Input Sanitization

```python
# backend/utils/sanitization.py

from bleach import clean
import re

def sanitize_user_input(text: str) -> str:
    """Remove potentially dangerous content from user input"""
    # Remove HTML tags
    text = clean(text, tags=[], strip=True)
    
    # Remove potential code injection
    text = re.sub(r'[;&|`$]', '', text)
    
    # Limit length
    return text[:10000]  # Max 10k chars

def sanitize_file_path(path: str) -> str:
    """Prevent path traversal attacks"""
    # Remove ../ and absolute paths
    path = path.replace('../', '').replace('..\\', '')
    if path.startswith('/'):
        raise ValueError("Absolute paths not allowed")
    return path
```

### 2. API Key Management

```python
# backend/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # OpenRouter
    openrouter_api_key: str
    default_llm_model: str = "google/gemini-2.5-pro"
    
    # MCP/Embeddings
    openai_api_key: str
    milvus_address: str
    milvus_token: str
    
    # Security
    allowed_origins: list[str] = ["http://localhost:3000"]
    session_timeout_minutes: int = 30
    max_message_length: int = 10000
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### 3. CORS Configuration

```python
# backend/main.py

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)
```

### 4. Rate Limiting

```python
# backend/middleware/rate_limit.py

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/conversations/message")
@limiter.limit("10/minute")  # Max 10 messages per minute
async def send_message(...):
    ...
```

### 5. Context Sanitization

```python
# backend/services/llm.py

def sanitize_context_for_llm(context: List[Dict]) -> List[Dict]:
    """Remove sensitive data before sending to OpenRouter"""
    sensitive_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # emails
        r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b',  # CPF
        r'\b(?:senha|password|token|secret)\s*[:=]\s*\S+',  # credentials
    ]
    
    for item in context:
        for pattern in sensitive_patterns:
            item['content'] = re.sub(pattern, '[REDACTED]', item['content'])
    
    return context
```

### 6. Session Security

```python
# backend/utils/session.py

import secrets
from datetime import datetime, timedelta

def generate_session_id() -> str:
    """Generate cryptographically secure session ID"""
    return f"sess_{secrets.token_urlsafe(32)}"

def is_session_expired(session: Session) -> bool:
    """Check if session has exceeded timeout"""
    timeout = timedelta(minutes=settings.session_timeout_minutes)
    return datetime.now() - session.last_activity > timeout

def cleanup_expired_sessions():
    """Periodically remove expired sessions"""
    expired = [
        sid for sid, session in sessions.items()
        if is_session_expired(session)
    ]
    for sid in expired:
        del sessions[sid]
```

---

## ⚡ Performance Optimization

### 1. Caching Strategy

```python
# backend/services/cache.py

from functools import lru_cache
from typing import List, Dict
import hashlib

class ContextCache:
    """In-memory cache for MCP search results"""
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, List[Dict]] = {}
        self.max_size = max_size
    
    def _generate_key(self, repo: str, query: str) -> str:
        return hashlib.sha256(f"{repo}:{query}".encode()).hexdigest()[:16]
    
    def get(self, repo: str, query: str) -> Optional[List[Dict]]:
        key = self._generate_key(repo, query)
        return self.cache.get(key)
    
    def set(self, repo: str, query: str, results: List[Dict]):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (FIFO)
            self.cache.pop(next(iter(self.cache)))
        
        key = self._generate_key(repo, query)
        self.cache[key] = results

context_cache = ContextCache()
```

### 2. Async Operations

```python
# backend/services/mcp.py

import asyncio
from typing import List

async def search_multiple_repositories(
    repositories: List[str],
    query: str
) -> Dict[str, List[Dict]]:
    """Search multiple repositories in parallel"""
    
    async def search_one(repo: str) -> tuple[str, List[Dict]]:
        results = await mcp_client.search_code(repo, query, limit=10)
        return repo, results
    
    # Execute searches in parallel
    tasks = [search_one(repo) for repo in repositories]
    results = await asyncio.gather(*tasks)
    
    return dict(results)
```

### 3. Streaming Responses

```python
# backend/api/conversations.py

from fastapi.responses import StreamingResponse

@app.post("/api/conversations/message/stream")
async def send_message_stream(request: SendMessageRequest):
    """Stream LLM response as it's generated"""
    
    async def generate():
        async for chunk in llm_client.chat_stream(
            messages=conversation_history
        ):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

### 4. Background Tasks

```python
# backend/api/analysis.py

from fastapi import BackgroundTasks

@app.post("/api/analysis/tech-debt")
async def analyze_tech_debt(
    request: AnalyzeTechDebtRequest,
    background_tasks: BackgroundTasks
):
    """Start analysis and return immediately"""
    
    # Return immediately
    analysis_id = f"analysis_{secrets.token_hex(8)}"
    
    # Run in background
    background_tasks.add_task(
        run_tech_debt_analysis,
        analysis_id,
        request.session_id,
        request.repository
    )
    
    return {"analysis_id": analysis_id, "status": "running"}
```

### 5. Prompt Optimization

```python
# backend/services/llm.py

def optimize_context_for_prompt(
    context: List[Dict],
    max_tokens: int = 4000
) -> List[Dict]:
    """Reduce context size to fit in token limit"""
    
    # Sort by relevance score
    sorted_context = sorted(
        context,
        key=lambda x: x.get('score', 0),
        reverse=True
    )
    
    # Add top results until token limit
    selected = []
    total_tokens = 0
    
    for item in sorted_context:
        estimated_tokens = len(item['content']) // 4  # rough estimate
        if total_tokens + estimated_tokens > max_tokens:
            break
        selected.append(item)
        total_tokens += estimated_tokens
    
    return selected
```

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Context Search** | < 3s | MCP search + ranking |
| **LLM Response** | < 5s | First token (streaming) |
| **Tech Debt Analysis** | < 15s | Full repository scan |
| **Page Load** | < 2s | Initial React render |
| **Session Creation** | < 500ms | In-memory operation |
| **Export Generation** | < 1s | Markdown formatting |

---

## 🧪 Testing Strategy

### 1. Unit Tests

```python
# tests/test_services/test_llm.py

import pytest
from backend.services.llm import LLMService, sanitize_context_for_llm

@pytest.mark.asyncio
async def test_llm_service_basic_chat():
    service = LLMService()
    response = await service.chat(
        messages=[{"role": "user", "content": "Hello"}]
    )
    assert response is not None
    assert len(response) > 0

def test_sanitize_context_removes_email():
    context = [{"content": "Contact: user@example.com"}]
    sanitized = sanitize_context_for_llm(context)
    assert "user@example.com" not in sanitized[0]["content"]
    assert "[REDACTED]" in sanitized[0]["content"]

def test_sanitize_context_removes_cpf():
    context = [{"content": "CPF: 123.456.789-00"}]
    sanitized = sanitize_context_for_llm(context)
    assert "123.456.789-00" not in sanitized[0]["content"]
```

```python
# tests/test_services/test_mcp.py

@pytest.mark.asyncio
async def test_mcp_search_returns_results(mcp_service):
    results = await mcp_service.search_code(
        repository="/path/to/repo",
        query="authentication",
        limit=5
    )
    assert len(results) <= 5
    assert all('file' in r for r in results)
    assert all('score' in r for r in results)
```

### 2. Integration Tests

```python
# tests/integration/test_conversation_flow.py

@pytest.mark.asyncio
async def test_full_conversation_flow(async_client):
    # 1. Create session
    response = await async_client.post("/api/sessions", json={
        "user_profile": "technical",
        "selected_repositories": ["/test/repo"]
    })
    assert response.status_code == 201
    session_id = response.json()["session_id"]
    
    # 2. Send message
    response = await async_client.post("/api/conversations/message", json={
        "session_id": session_id,
        "message": "Add caching to the API"
    })
    assert response.status_code == 200
    assert "assistant_reply" in response.json()
    
    # 3. Analyze tech debt
    response = await async_client.post("/api/analysis/tech-debt", json={
        "session_id": session_id
    })
    assert response.status_code == 200
    assert "total_items" in response.json()
    
    # 4. Export spec
    response = await async_client.post("/api/export", json={
        "session_id": session_id,
        "format": "markdown"
    })
    assert response.status_code == 200
    assert "specs" in response.json()
```

### 3. E2E Tests (Playwright)

```typescript
// tests/e2e/create-spec.spec.ts

import { test, expect } from '@playwright/test';

test('complete spec creation flow', async ({ page }) => {
  // 1. Open app
  await page.goto('http://localhost:3000');
  
  // 2. Select profile
  await page.click('[data-testid="profile-technical"]');
  
  // 3. Select repository
  await page.click('[data-testid="repo-backend"]');
  
  // 4. Type feature description
  await page.fill('[data-testid="feature-input"]', 
    'Add Redis caching to SIGTAP service'
  );
  await page.click('[data-testid="send-button"]');
  
  // 5. Wait for AI response
  await expect(page.locator('[data-testid="ai-response"]'))
    .toBeVisible({ timeout: 10000 });
  
  // 6. Check preview is updating
  await expect(page.locator('[data-testid="spec-preview"]'))
    .toContainText('Redis');
  
  // 7. Run tech debt analysis
  await page.click('[data-testid="tech-debt-button"]');
  await expect(page.locator('[data-testid="tech-debt-results"]'))
    .toBeVisible({ timeout: 20000 });
  
  // 8. Export
  await page.click('[data-testid="export-button"]');
  const downloadPromise = page.waitForEvent('download');
  await page.click('[data-testid="download-md"]');
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toMatch(/\.md$/);
});
```

### 4. Load Tests (Locust)

```python
# tests/load/locustfile.py

from locust import HttpUser, task, between

class Context2TaskUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Create session
        response = self.client.post("/api/sessions", json={
            "user_profile": "technical",
            "selected_repositories": ["/test/repo"]
        })
        self.session_id = response.json()["session_id"]
    
    @task(3)
    def send_message(self):
        self.client.post("/api/conversations/message", json={
            "session_id": self.session_id,
            "message": "Add feature X"
        })
    
    @task(1)
    def analyze_tech_debt(self):
        self.client.post("/api/analysis/tech-debt", json={
            "session_id": self.session_id
        })
```

---

## 🚀 Deployment Strategy

### Docker Compose Setup

```yaml
# docker-compose.yml

version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000/ws
    depends_on:
      - backend
    networks:
      - context2task-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MILVUS_ADDRESS=${MILVUS_ADDRESS}
      - MILVUS_TOKEN=${MILVUS_TOKEN}
      - ALLOWED_ORIGINS=http://localhost:3000
    volumes:
      - ./backend:/app
      - node_modules:/app/node_modules  # For MCP npx
    networks:
      - context2task-network

networks:
  context2task-network:
    driver: bridge

volumes:
  node_modules:
```

### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile

# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Backend Dockerfile

```dockerfile
# backend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Install Node.js (for MCP)
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Environment Variables

```bash
# .env

# OpenRouter (LLM)
OPENROUTER_API_KEY=sk-or-v1-xxxxx
DEFAULT_LLM_MODEL=google/gemini-2.5-pro
FALLBACK_MODELS=anthropic/claude-3.5-sonnet,openai/gpt-4o

# MCP/Embeddings
OPENAI_API_KEY=sk-proj-xxxxx
MILVUS_ADDRESS=https://in03-xxx.serverless.gcp-us-west1.cloud.zilliz.com
MILVUS_TOKEN=092c834ce630c1dc...

# App Config
APP_NAME=Context2Task
APP_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000

# Security
SESSION_TIMEOUT_MINUTES=30
MAX_MESSAGE_LENGTH=10000
RATE_LIMIT_PER_MINUTE=60

# Performance
CONTEXT_CACHE_SIZE=1000
MAX_CONTEXT_TOKENS=4000
```

### Startup Script

```bash
#!/bin/bash
# scripts/start.sh

set -e

echo "🚀 Starting Context2Task..."

# Check .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Copy .env.example to .env and configure"
    exit 1
fi

# Pull latest images
echo "📦 Pulling images..."
docker-compose pull

# Build containers
echo "🔨 Building containers..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for backend to be ready
echo "⏳ Waiting for backend..."
until curl -s http://localhost:8000/health > /dev/null; do
    sleep 1
done

echo "✅ Context2Task is running!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
```

---

## ⚠️ Risks & Mitigation

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **MCP Server Instability** | High | Medium | Fallback to direct code analysis; retry logic; health checks |
| **OpenRouter Rate Limits** | Medium | Low | Request queuing; backoff strategy; cost monitoring |
| **Large Codebase Indexing** | Medium | High | Progressive indexing; chunk limits; timeout handling |
| **Session Memory Overflow** | Medium | Medium | Auto-cleanup expired sessions; max sessions per instance |
| **LLM Response Quality** | High | Medium | Prompt engineering; temperature tuning; multi-model fallback |
| **Context Token Limits** | Medium | High | Smart context selection; token counting; chunking strategy |

### Operational Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **API Key Exposure** | Critical | Low | Environment variables; .gitignore; secrets management |
| **High Latency** | Medium | Medium | Caching; async operations; streaming responses |
| **Data Loss (In-Memory)** | Low | High | Expected behavior V1; document to users; V2 adds persistence |
| **CORS Issues** | Low | Medium | Proper configuration; testing; documentation |
| **Docker Build Failures** | Medium | Low | Multi-stage builds; layer caching; CI/CD validation |

### Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Low Adoption** | High | Medium | User training; interactive tutorial; template library |
| **Poor Spec Quality** | High | Medium | Iterative prompt improvement; user feedback loop; validation |
| **Cost Overrun (LLM)** | Medium | Medium | Token optimization; prompt caching; usage monitoring |
| **Slow Time-to-Value** | Medium | Low | Quick setup (<2min); pre-configured templates; examples |

---

## 📦 Dependency Management

### Frontend Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@radix-ui/react-*": "latest",
    "tailwindcss": "^3.3.0",
    "zustand": "^4.4.0",
    "@tanstack/react-query": "^5.0.0",
    "socket.io-client": "^4.6.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "react-markdown": "^9.0.0",
    "remark-gfm": "^4.0.0",
    "mermaid": "^10.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "eslint": "^8.54.0",
    "prettier": "^3.1.0",
    "@playwright/test": "^1.40.0"
  }
}
```

### Backend Dependencies

```txt
# requirements.txt

fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.0
python-multipart==0.0.6
python-dotenv==1.0.0
structlog==23.2.0
pytest==7.4.3
pytest-asyncio==0.21.1
slowapi==0.1.9
bleach==6.1.0
websockets==12.0
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml

name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm test
      - name: Build
        run: |
          cd frontend
          npm run build

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [test-backend, test-frontend]
    steps:
      - uses: actions/checkout@v3
      - name: Start services
        run: docker-compose up -d
      - name: Run E2E tests
        run: npx playwright test
      - name: Stop services
        run: docker-compose down
```

---

## 📊 Monitoring & Observability

### Logging Strategy

```python
# backend/utils/logging.py

import structlog

def configure_logging():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )

logger = structlog.get_logger()

# Usage
logger.info("session_created", session_id=session_id, user_profile=profile)
logger.error("mcp_search_failed", repository=repo, error=str(e))
```

### Health Checks

```python
# backend/api/health.py

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    
    checks = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "openrouter": await check_openrouter(),
            "mcp": await check_mcp(),
            "sessions": len(sessions)
        }
    }
    
    if any(not v for k, v in checks["services"].items() if k != "sessions"):
        checks["status"] = "degraded"
    
    return checks
```

---

## 📅 Implementation Roadmap

### Phase 1: Core MVP (2 weeks)

**Week 1**:
- ✅ Docker setup (frontend + backend containers)
- ✅ Basic FastAPI structure + session management
- ✅ React setup with shadcn/ui
- ✅ MCP client integration (search_code)
- ✅ OpenRouter LLM integration

**Week 2**:
- ✅ Chat interface with conversation history
- ✅ Basic spec generation (company template)
- ✅ Profile selection (technical vs non-technical)
- ✅ Multi-repository support
- ✅ Export to Markdown

### Phase 2: Analysis Features (1 week)

- ✅ Tech Debt Detector (IA-based)
- ✅ Security Checklist
- ✅ Mermaid Diagram generation
- ✅ Integration with analysis workflow

### Phase 3: Advanced Features (1 week)

- ✅ Multi-spec automatic detection and generation
- ✅ Voice input (Web Speech API)
- ✅ Markdown preview side-by-side
- ✅ GitHub Projects integration
- ✅ Template system

### Phase 4: Polish & Testing (1 week)

- ✅ E2E tests (Playwright)
- ✅ Performance optimization
- ✅ Error handling and edge cases
- ✅ Documentation
- ✅ User testing and feedback

**Total: ~5 weeks for production-ready V1**

---

## 📚 Documentation Plan

### User Documentation
1. **README.md**: Setup, quick start, features overview
2. **USER_GUIDE.md**: Step-by-step usage guide with screenshots
3. **TEMPLATES.md**: How to customize templates
4. **FAQ.md**: Common questions and troubleshooting

### Developer Documentation
1. **ARCHITECTURE.md**: System design, components, data flow
2. **API_REFERENCE.md**: Complete API documentation (auto-generated from OpenAPI)
3. **DEPLOYMENT.md**: Docker setup, environment variables, deployment guide
4. **CONTRIBUTING.md**: Development setup, coding standards, PR process

### Operations Documentation
1. **MONITORING.md**: Logging, health checks, alerts
2. **TROUBLESHOOTING.md**: Common issues and solutions
3. **SCALING.md**: How to scale (V2 with Redis, multiple instances)

---

## ✅ Definition of Done

### MVP Ready When:
- ✅ `docker-compose up` starts the application successfully
- ✅ User can create a session and chat with AI
- ✅ System generates complete spec in company format
- ✅ Multi-repository context works correctly
- ✅ Tech debt analysis returns meaningful results
- ✅ Export to Markdown produces correct format
- ✅ All critical paths have unit + integration tests
- ✅ E2E test covers full flow from start to export
- ✅ Performance targets are met (< 3s context search, < 5s LLM response)
- ✅ Security checklist implemented (CORS, sanitization, rate limiting)
- ✅ Documentation is complete and accurate
- ✅ No critical bugs in production-critical paths

---

**Status**: Ready for Implementation  
**Tech Lead**: TBD  
**Created**: 2025-10-19  
**Last Updated**: 2025-10-19  
**Review Status**: Pending Review

