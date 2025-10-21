# Context2Task - Roadmap de Implementação Detalhado

**Data**: 2025-10-19  
**Versão**: 1.0  
**Propósito**: Guia passo-a-passo para implementação do MVP até V2

---

## 📊 Visão Geral

### Timeline Estimado
- **Fase 1 (MVP)**: 3 semanas (core functionality)
- **Fase 2 (Polish)**: 1 semana (UX + testing)
- **Fase 3 (Advanced)**: 2 semanas (features avançadas)
- **TOTAL**: ~6 semanas para V1 completo

### Priorização
- **P0 (Crítico)**: Sem isso, produto não funciona
- **P1 (Alto)**: Impacto significativo na UX
- **P2 (Médio)**: Nice to have para V1
- **P3 (Baixo)**: V2+

---

## 🏗️ FASE 1: MVP Core (Semanas 1-3)

### Sprint 1: Fundação (Dias 1-5)

#### 📦 Task 1.1: Docker Setup (P0) - 1 dia
**Objetivo**: Ambiente local funcionando com 1 comando

**Deliverables**:
- `docker-compose.yml` completo
- Frontend Dockerfile (multi-stage build)
- Backend Dockerfile (Python 3.10+)
- `.env.example` com todas variáveis
- `scripts/start.sh` e `scripts/stop.sh`
- `README.md` com instruções

**Validação**:
```bash
$ docker-compose up
# ✅ Frontend acessível em localhost:3000
# ✅ Backend acessível em localhost:8000
# ✅ Health check passing
```

**Files**:
```
/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   └── nginx.conf
├── backend/
│   ├── Dockerfile
│   └── requirements.txt
└── scripts/
    ├── start.sh
    └── stop.sh
```

---

#### 🎨 Task 1.2: Frontend Base (P0) - 2 dias
**Objetivo**: React app com shadcn/ui configurado

**Deliverables**:
- React 18 + TypeScript + Vite
- shadcn/ui instalado e configurado
- Tailwind CSS setup
- Estrutura de pastas
- Componentes base (Button, Input, Card, etc.)
- Routing (React Router)
- State management (Zustand)

**Estrutura**:
```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/            # shadcn components
│   │   ├── chat/
│   │   ├── sidebar/
│   │   └── preview/
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Session.tsx
│   │   └── Review.tsx
│   ├── stores/
│   │   └── session.ts     # Zustand store
│   ├── api/
│   │   └── client.ts      # API client
│   └── types/
│       └── index.ts       # TypeScript types
```

**Validação**:
- ✅ Componentes renderizam corretamente
- ✅ Tema dark/light funciona
- ✅ Navegação entre páginas OK
- ✅ TypeScript sem erros

---

#### ⚙️ Task 1.3: Backend Base (P0) - 2 dias
**Objetivo**: FastAPI funcionando com estrutura base

**Deliverables**:
- FastAPI app
- Estrutura de pastas
- Session management (in-memory)
- Basic endpoints (health, sessions)
- CORS configurado
- Logging estruturado (structlog)
- Error handling

**Estrutura**:
```
backend/
├── main.py                # FastAPI app
├── api/
│   ├── sessions.py
│   ├── conversations.py
│   └── analysis.py
├── models/
│   ├── session.py
│   ├── message.py
│   └── spec.py
├── services/
│   ├── llm.py            # OpenRouter client
│   ├── mcp.py            # MCP client
│   └── spec_generator.py
├── utils/
│   ├── logging.py
│   ├── sanitization.py
│   └── validation.py
├── config.py
└── tests/
```

**Validação**:
```bash
$ curl http://localhost:8000/health
{"status": "healthy"}

$ curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_profile": "technical", "selected_repositories": ["/test"]}'
{"session_id": "sess_abc123", ...}
```

---

### Sprint 2: Integrations (Dias 6-10)

#### 🔌 Task 2.1: OpenRouter Integration (P0) - 1 dia
**Objetivo**: LLM funcionando com Gemini 2.5 Pro

**Deliverables**:
- OpenRouter client configurado
- Prompt templates implementados
- Streaming support
- Error handling + retry logic
- Token counting
- Cost tracking

**Code Example**:
```python
# backend/services/llm.py

from openai import AsyncOpenAI
from typing import List, Dict, AsyncGenerator

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key
        )
        self.model = settings.default_llm_model
    
    async def chat(
        self,
        messages: List[Dict],
        stream: bool = False
    ) -> Dict | AsyncGenerator:
        """Chat with LLM"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream,
                extra_headers={
                    "HTTP-Referer": settings.app_url,
                    "X-Title": settings.app_name
                }
            )
            
            if stream:
                return self._stream_response(response)
            else:
                return self._parse_response(response)
                
        except Exception as e:
            logger.error("llm_error", error=str(e))
            raise
    
    async def _stream_response(self, response):
        """Stream chunks"""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

**Validação**:
- ✅ Consegue fazer chat simples
- ✅ Streaming funciona
- ✅ Retry em rate limit
- ✅ Logs estruturados

---

#### 🔍 Task 2.2: MCP Integration (P0) - 2 dias
**Objetivo**: Busca de contexto funcionando

**Deliverables**:
- MCP client (subprocess communication)
- Métodos: index, search, clear, status
- Error handling para MCP offline
- Caching de resultados
- Ranking de relevância

**Code Example**:
```python
# backend/services/mcp.py

import asyncio
import json
from typing import List, Dict

class MCPClient:
    def __init__(self):
        self.process = None
        self.request_id = 0
    
    async def start(self):
        """Start MCP server process"""
        self.process = await asyncio.create_subprocess_exec(
            "npx", "-y", "@zilliz/claude-context-mcp@latest",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={
                "OPENAI_API_KEY": settings.openai_api_key,
                "MILVUS_ADDRESS": settings.milvus_address,
                "MILVUS_TOKEN": settings.milvus_token
            }
        )
        
        logger.info("mcp_started", pid=self.process.pid)
    
    async def search_code(
        self,
        repository: str,
        query: str,
        limit: int = 10
    ) -> List[Dict]:
        """Search code in repository"""
        
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": "search_code",
                "arguments": {
                    "path": repository,
                    "query": query,
                    "limit": limit
                }
            }
        }
        
        # Send request
        self.process.stdin.write(
            json.dumps(request).encode() + b'\n'
        )
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode())
        
        if "error" in response:
            raise MCPError(response["error"])
        
        results = response.get("result", [])
        
        logger.info(
            "mcp_search_completed",
            query=query,
            results_count=len(results)
        )
        
        return results
```

**Validação**:
- ✅ Consegue buscar código
- ✅ Resultados relevantes (score > 0.7)
- ✅ Fallback se MCP offline
- ✅ Latência < 3s

---

#### 💬 Task 2.3: Chat Flow (P0) - 2 dias
**Objetivo**: Conversa básica funcionando

**Deliverables**:
- Endpoint de mensagens
- Histórico de conversa
- Enriquecimento com MCP
- Geração de respostas
- Atualização de spec progressivamente

**Flow**:
```
User sends message
  ↓
Backend receives
  ↓
MCP search (contexto)
  ↓
Build prompt (system + context + history + message)
  ↓
LLM generate response
  ↓
Update spec document
  ↓
Return response + spec_updates
  ↓
Frontend updates UI
```

**API**:
```
POST /api/conversations/message
{
  "session_id": "sess_xxx",
  "message": "Quero cache Redis"
}

Response:
{
  "message_id": "msg_yyy",
  "assistant_reply": "Entendi! Vou ajudar...",
  "context_used": [
    {
      "file": "backend/cache.py",
      "score": 0.92
    }
  ],
  "spec_updates": {
    "description": "Implementar cache Redis...",
    "technical_details": ["Item 1", "Item 2"]
  }
}
```

**Validação**:
- ✅ Conversa multi-turno funciona
- ✅ Contexto é usado nas respostas
- ✅ Spec é atualizada progressivamente
- ✅ Histórico é mantido

---

### Sprint 3: Spec Generation (Dias 11-15)

#### 📝 Task 3.1: Spec Generator (P0) - 2 dias
**Objetivo**: Gerar documento no formato da empresa

**Deliverables**:
- Template engine (usar company-task-template.md)
- Preenchimento progressivo
- Validação de completude
- Formatação Markdown

**Code Example**:
```python
# backend/services/spec_generator.py

class SpecGenerator:
    def __init__(self):
        with open("company-task-template.md") as f:
            self.template = f.read()
    
    def generate_spec(self, spec_data: SpecDocument) -> str:
        """Generate markdown from spec data"""
        
        sections = {
            "description": spec_data.description,
            "user_story": spec_data.user_story,
            "expected_results": self._format_list(spec_data.expected_results),
            "technical_details": self._format_list(spec_data.technical_details),
            "checklist": self._format_checklist(spec_data.checklist),
            "acceptance_criteria": self._format_list(spec_data.acceptance_criteria),
            "definition_of_done": self._format_list(spec_data.definition_of_done),
            "observations": spec_data.observations or "",
            "references": self._format_list(spec_data.references) if spec_data.references else "",
            "risks": self._format_list(spec_data.risks) if spec_data.risks else ""
        }
        
        # Replace template variables
        result = self.template
        for key, value in sections.items():
            result = result.replace(f"{{{key}}}", value)
        
        return result
    
    def validate_completeness(self, spec_data: SpecDocument) -> Dict:
        """Check how complete the spec is"""
        
        required_fields = [
            "description",
            "user_story",
            "expected_results",
            "technical_details",
            "acceptance_criteria"
        ]
        
        completed = sum(
            1 for field in required_fields
            if getattr(spec_data, field)
        )
        
        return {
            "total_fields": len(required_fields),
            "completed_fields": completed,
            "percentage": (completed / len(required_fields)) * 100,
            "missing_fields": [
                f for f in required_fields
                if not getattr(spec_data, f)
            ]
        }
```

**Validação**:
- ✅ Markdown gerado é válido
- ✅ Todas seções presentes
- ✅ Formatação correta
- ✅ Emojis renderizam

---

#### 🎯 Task 3.2: Profile Adaptation (P0) - 1 dia
**Objetivo**: IA adapta linguagem ao perfil

**Deliverables**:
- System prompts por perfil
- Validação de output por perfil
- Testes com ambos perfis

**Implementation**:
```python
# backend/services/conversation.py

class ConversationService:
    def __init__(self, llm: LLMService, mcp: MCPClient):
        self.llm = llm
        self.mcp = mcp
        self.prompts = PromptLibrary()
    
    async def process_message(
        self,
        session: Session,
        message: str
    ) -> Dict:
        """Process user message"""
        
        # Get context from MCP
        context = await self.mcp.search_code(
            repository=session.selected_repositories[0].path,
            query=message,
            limit=10
        )
        
        # Build messages for LLM
        messages = [
            {
                "role": "system",
                "content": self.prompts.system_prompt(session.user_profile)
            },
            *self._format_history(session.conversation_history),
            {
                "role": "user",
                "content": self.prompts.user_message_prompt(
                    message=message,
                    context=context,
                    profile=session.user_profile
                )
            }
        ]
        
        # Get LLM response
        response = await self.llm.chat(messages)
        
        # Parse and extract spec updates
        spec_updates = self._extract_spec_updates(response)
        
        return {
            "assistant_reply": response["content"],
            "context_used": context,
            "spec_updates": spec_updates
        }
```

**Validação**:
- ✅ Não-técnico recebe linguagem simples
- ✅ Técnico recebe detalhes técnicos
- ✅ Tradeoffs adaptados ao perfil

---

#### 📥 Task 3.3: Export (P0) - 1 dia
**Objetivo**: Download de markdown

**Deliverables**:
- Endpoint de export
- Download de arquivo .md
- Copy to clipboard (frontend)
- Formatos: MD, JSON, YAML

**API**:
```
POST /api/export
{
  "session_id": "sess_xxx",
  "format": "markdown"
}

Response:
{
  "specs": {
    "backend-api": "# 📌 Descrição..."
  }
}
```

**Frontend**:
```typescript
// Download MD
const downloadMd = async () => {
  const response = await api.export(sessionId, 'markdown');
  const blob = new Blob([response.specs['backend-api']], 
    { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'spec.md';
  a.click();
};

// Copy to clipboard
const copyToClipboard = async () => {
  const response = await api.export(sessionId, 'markdown');
  await navigator.clipboard.writeText(response.specs['backend-api']);
  toast.success('Copiado!');
};
```

**Validação**:
- ✅ Download funciona
- ✅ Copy funciona
- ✅ Formatos diferentes OK

---

## 🎨 FASE 2: Polish & Testing (Semana 4)

### Sprint 4: UX & Features (Dias 16-20)

#### 🎤 Task 4.1: Voice Input (P1) - 2 dias
**Objetivo**: Usuário pode falar ao invés de digitar

**Deliverables**:
- Web Speech API integration
- Transcrição em tempo real
- UI de gravação
- Fallback para Whisper API (opcional)

**Frontend**:
```typescript
// components/VoiceInput.tsx

import { useState, useRef } from 'react';

const VoiceInput = ({ onTranscript }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef(null);
  
  const startRecording = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      alert('Navegador não suporta reconhecimento de voz');
      return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'pt-BR';
    recognition.continuous = true;
    recognition.interimResults = true;
    
    recognition.onresult = (event) => {
      const current = event.resultIndex;
      const transcript = event.results[current][0].transcript;
      setTranscript(transcript);
    };
    
    recognition.start();
    setIsRecording(true);
    recognitionRef.current = recognition;
  };
  
  const stopRecording = () => {
    recognitionRef.current?.stop();
    setIsRecording(false);
    onTranscript(transcript);
  };
  
  return (
    <div>
      {!isRecording ? (
        <Button onClick={startRecording}>
          🎤 Falar
        </Button>
      ) : (
        <div>
          <div className="recording-indicator">
            🔴 Gravando... {transcript}
          </div>
          <Button onClick={stopRecording}>
            ⏹️ Parar
          </Button>
        </div>
      )}
    </div>
  );
};
```

**Validação**:
- ✅ Grava e transcreve em português
- ✅ Mostra transcrição em tempo real
- ✅ UI clara e intuitiva
- ✅ Fallback se não suportado

---

#### 📊 Task 4.2: Preview Side-by-Side (P1) - 1 dia
**Objetivo**: Ver documento sendo construído

**Deliverables**:
- Split view (chat + preview)
- Markdown rendering (react-markdown)
- Auto-scroll to latest section
- Toggle entre modos (chat-only, split, preview-only)

**Frontend**:
```typescript
// components/PreviewPane.tsx

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const PreviewPane = ({ markdown }) => {
  return (
    <div className="preview-pane">
      <div className="preview-header">
        <h3>📄 Preview do Documento</h3>
        <div className="completeness-badge">
          90% completo
        </div>
      </div>
      
      <ReactMarkdown 
        remarkPlugins={[remarkGfm]}
        className="markdown-body"
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
};
```

**Validação**:
- ✅ Preview atualiza em tempo real
- ✅ Markdown renderiza corretamente
- ✅ Scroll automático funciona
- ✅ Toggle entre modos OK

---

#### ⚠️ Task 4.3: Tech Debt Detector (P1) - 2 dias
**Objetivo**: Análise inteligente de dívida técnica

**Deliverables**:
- Endpoint de análise
- Prompt especializado
- Classificação por severidade
- UI de resultados

**Backend**:
```python
# backend/api/analysis.py

@app.post("/api/analysis/tech-debt")
async def analyze_tech_debt(
    request: AnalyzeTechDebtRequest,
    background_tasks: BackgroundTasks
):
    """Analyze tech debt using AI"""
    
    session = sessions.get(request.session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    # Get code context
    code_context = []
    for repo in session.selected_repositories:
        results = await mcp_client.search_code(
            repository=repo.path,
            query=f"{session.specs[repo.name].title} {session.specs[repo.name].description}",
            limit=15
        )
        code_context.extend(results)
    
    # Build specialized prompt
    prompt = prompts.tech_debt_analysis_prompt(
        feature_title=session.specs[repo.name].title,
        code_context=code_context,
        tech_stack=session.tech_stack
    )
    
    # Call LLM
    response = await llm_service.chat([
        {"role": "system", "content": "You are a senior software architect"},
        {"role": "user", "content": prompt}
    ])
    
    # Parse JSON response
    analysis = json.loads(response["content"])
    
    return AnalyzeTechDebtResponse(
        total_items=analysis["summary"]["total_issues"],
        critical=analysis["tech_debt"][:3],  # Top 3 critical
        medium=analysis["tech_debt"][3:6],
        low=analysis["tech_debt"][6:],
        total_effort_hours=analysis["summary"]["total_effort_hours"]
    )
```

**Frontend UI**:
```typescript
// components/TechDebtReport.tsx

const TechDebtReport = ({ analysis }) => {
  return (
    <div className="tech-debt-report">
      <div className="summary">
        📊 {analysis.total_items} problemas | 
        {analysis.total_effort_hours}h esforço total
      </div>
      
      {analysis.critical.length > 0 && (
        <div className="section critical">
          <h3>🔴 Críticos ({analysis.critical.length})</h3>
          {analysis.critical.map(item => (
            <TechDebtItem key={item.file} item={item} />
          ))}
        </div>
      )}
      
      {/* Similar for medium and low */}
      
      <div className="actions">
        <Button onClick={addAllToSpec}>
          ✅ Adicionar Todos à Spec
        </Button>
        <Button variant="outline" onClick={selectItems}>
          ⚙️ Selecionar
        </Button>
      </div>
    </div>
  );
};
```

**Validação**:
- ✅ Análise retorna problemas reais
- ✅ Classificação por severidade correta
- ✅ Sugestões são acionáveis
- ✅ UI clara e navegável

---

## 🚀 FASE 3: Advanced Features (Semanas 5-6)

### Sprint 5: Multi-Spec & Review (Dias 21-25)

#### 🔢 Task 5.1: Multi-Spec Detection (P1) - 3 dias
**Objetivo**: Detectar quando precisa múltiplas specs

**Deliverables**:
- Análise de impacto multi-repo
- Detecção automática (não-técnico)
- Detecção manual (técnico)
- Geração de specs linkadas
- Export coordenado

**Validação**:
- ✅ Detecta corretamente (>90% accuracy)
- ✅ Gera specs separadas
- ✅ Linking entre specs funciona
- ✅ Export cria arquivos linkados

---

#### ✅ Task 5.2: Review Mode (P2) - 2 dias
**Objetivo**: Workflow de aprovação

**Deliverables**:
- Estados: Draft → Review → Approved
- @mentions
- Comentários inline
- Página separada de review

**Validação**:
- ✅ Transições de estado funcionam
- ✅ @mentions notificam
- ✅ Comentários salvos
- ✅ Aprovação registrada

---

### Sprint 6: Final Polish (Dias 26-30)

#### 🔒 Task 6.1: Security Checklist (P1) - 1 dia
#### 📊 Task 6.2: Mermaid Diagrams (P2) - 1 dia
#### 🎓 Task 6.3: Interactive Tutorial (P1) - 1 dia
#### 🧪 Task 6.4: E2E Testing (P0) - 2 dias

---

## 📋 Definition of Done para MVP

### Core Functionality
- [x] Docker compose up funciona
- [ ] Chat multi-turno OK
- [ ] MCP busca contexto relevante
- [ ] LLM gera respostas adaptadas ao perfil
- [ ] Spec é gerada no formato da empresa
- [ ] Export para markdown funciona

### Advanced Features
- [ ] Voice input funciona
- [ ] Preview side-by-side OK
- [ ] Tech debt analysis retorna resultados úteis
- [ ] Multi-spec detecta corretamente

### Quality
- [ ] > 80% test coverage
- [ ] E2E tests passam
- [ ] Performance targets OK (< 3s MCP, < 5s LLM)
- [ ] Sem erros críticos

### Documentation
- [ ] README com setup instructions
- [ ] API docs (auto-generated)
- [ ] User guide básico

---

**Próximo Passo**: Executar `/tasks` para gerar tasks implementáveis

