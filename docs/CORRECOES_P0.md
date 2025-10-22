# Plano de Correções P0 - Context2Task

**Objetivo:** Fazer o sistema funcionar com funcionalidades básicas  
**Prazo estimado:** 1-2 dias de trabalho focado  
**Prioridade:** CRÍTICA

---

## 🎯 CORREÇÃO #1: Dependências Python

### Problema
Dependências não estão instaladas (FastAPI, LangGraph, etc)

### Solução

**Opção A: Desenvolvimento local (sem Docker)**
```bash
cd context-coder/backend

# Instalar Poetry se não tiver
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell

# Testar
python main.py
```

**Opção B: Docker (recomendado)**
```bash
cd context-coder

# Rebuild sem cache
docker-compose build --no-cache backend

# Subir
docker-compose up backend
```

### Validação
```bash
# Deve retornar status 200
curl http://localhost:8000/health
```

---

## 🎯 CORREÇÃO #2: Dockerfile do Backend + Node.js

### Problema
MCP precisa de Node.js mas Dockerfile só tem Python

### Solução

Atualizar `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# ===== INSTALAR NODE.JS 20+ =====
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verificar instalação
RUN node --version && npm --version

# ===== INSTALAR POETRY =====
RUN pip install poetry==1.7.1

# Configurar Poetry para não criar virtualenv (já estamos em container)
RUN poetry config virtualenvs.create false

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências Python
RUN poetry install --no-interaction --no-ansi --no-root

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 8000

# Comando de início
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Validação
```bash
# Rebuild
docker-compose build --no-cache backend

# Verificar Node.js dentro do container
docker-compose run backend node --version
# Deve retornar: v20.x.x

docker-compose run backend npx --version
# Deve retornar: 10.x.x
```

---

## 🎯 CORREÇÃO #3: MCP Service com Fallback

### Problema
MCP falha silenciosamente quando Node.js não está disponível ou quando indexação demora

### Solução

Atualizar `backend/services/mcp.py`:

```python
"""
MCP Service - Model Context Protocol Integration
Communication with zilliztech/claude-context via npx
"""
import os
import json
import asyncio
import logging
import shutil
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class MCPService:
    """MCP Service with fallback and error handling"""
    
    def __init__(self):
        # Validate Node.js installation
        if not shutil.which("node") or not shutil.which("npx"):
            logger.error("Node.js/npx not found! MCP will run in FALLBACK MODE")
            self.mcp_available = False
        else:
            node_version = self._check_node_version()
            if node_version and node_version >= 20:
                self.mcp_available = True
                logger.info(f"MCP Service initialized (Node.js v{node_version})")
            else:
                logger.warning(f"Node.js version too old ({node_version}), need v20+")
                self.mcp_available = False
        
        # Validate required env vars
        required_vars = ["OPENAI_API_KEY", "ZILLIZ_CLOUD_URI", "ZILLIZ_CLOUD_API_KEY"]
        missing = [v for v in required_vars if not os.getenv(v)]
        if missing:
            logger.error(f"Missing env vars: {', '.join(missing)}")
            self.mcp_available = False
        
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.zilliz_uri = os.getenv("ZILLIZ_CLOUD_URI")
        self.zilliz_key = os.getenv("ZILLIZ_CLOUD_API_KEY")
    
    def _check_node_version(self) -> Optional[int]:
        """Check Node.js major version"""
        try:
            result = os.popen("node --version").read().strip()
            # Parse "v20.11.0" -> 20
            version = int(result.lstrip('v').split('.')[0])
            return version
        except Exception:
            return None
    
    async def _run_npx_command(
        self, 
        command: str, 
        args: List[str],
        timeout: int = 300  # 5 minutes for indexing
    ) -> Dict[str, Any]:
        """
        Run npx @zilliztech/claude-context command with timeout
        """
        if not self.mcp_available:
            raise RuntimeError("MCP not available (Node.js not installed)")
        
        # Build full command
        cmd = ["npx", "@zilliztech/claude-context", command] + args
        
        # Set environment
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = self.openai_key
        env["ZILLIZ_CLOUD_URI"] = self.zilliz_uri
        env["ZILLIZ_CLOUD_API_KEY"] = self.zilliz_key
        
        try:
            logger.info(f"Running MCP command: {command} (timeout: {timeout}s)")
            
            # Run command with timeout
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                raise RuntimeError(f"MCP command timed out after {timeout}s")
            
            if process.returncode != 0:
                error_msg = stderr.decode()
                logger.error(f"MCP command failed: {error_msg}")
                raise RuntimeError(f"MCP command failed: {error_msg}")
            
            # Parse JSON output
            output = stdout.decode()
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                # If not JSON, return raw output
                return {"output": output}
        
        except Exception as e:
            logger.error(f"MCP command execution error: {e}")
            raise
    
    async def search_code(
        self, 
        path: str, 
        query: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search code with fallback to simple file search
        """
        if not self.mcp_available:
            logger.warning("MCP unavailable, using fallback search")
            return await self._fallback_search(path, query, limit)
        
        try:
            result = await self._run_npx_command(
                "search-code",
                ["--path", path, "--query", query, "--limit", str(limit)],
                timeout=30  # 30s for search
            )
            
            return result.get("results", [])
        
        except Exception as e:
            logger.error(f"MCP search failed: {e}, using fallback")
            return await self._fallback_search(path, query, limit)
    
    async def _fallback_search(
        self, 
        path: str, 
        query: str, 
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Fallback: simple grep-based search
        """
        try:
            # Simple grep command
            cmd = [
                "grep",
                "-r",
                "-i",  # case insensitive
                "-n",  # line numbers
                "--include=*.py",
                "--include=*.ts",
                "--include=*.tsx",
                "--include=*.js",
                "--include=*.jsx",
                query,
                path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=10)
            
            # Parse grep output
            results = []
            for line in stdout.decode().split('\n')[:limit]:
                if ':' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        results.append({
                            "file": parts[0],
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "content": parts[2],
                            "score": 1.0
                        })
            
            logger.info(f"Fallback search found {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"Fallback search failed: {e}")
            return []
    
    async def index_codebase(
        self, 
        path: str, 
        force: bool = False
    ) -> Dict[str, Any]:
        """
        Index codebase with MCP (long operation)
        """
        if not self.mcp_available:
            return {
                "status": "error",
                "message": "MCP not available (Node.js required)"
            }
        
        try:
            args = ["--path", path]
            if force:
                args.append("--force")
            
            result = await self._run_npx_command(
                "index-codebase",
                args,
                timeout=600  # 10 minutes for large codebases
            )
            
            return {
                "status": "success",
                "path": path,
                "file_count": result.get("file_count", 0)
            }
        
        except Exception as e:
            logger.error(f"Indexing failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }


# Singleton instance
_mcp_service = None

def get_mcp_service() -> MCPService:
    """Get MCP service singleton"""
    global _mcp_service
    if _mcp_service is None:
        _mcp_service = MCPService()
    return _mcp_service
```

### Validação
```bash
# Testar dentro do container
docker-compose run backend python -c "
from services.mcp import get_mcp_service
import asyncio

async def test():
    mcp = get_mcp_service()
    print(f'MCP Available: {mcp.mcp_available}')
    
    # Test fallback search
    results = await mcp.search_code('/app', 'FastAPI', limit=5)
    print(f'Found {len(results)} results')

asyncio.run(test())
"
```

---

## 🎯 CORREÇÃO #4: SessionId no Frontend

### Problema
`sessionId` não é gerado automaticamente

### Solução

Atualizar `frontend/src/stores/session.ts`:

```typescript
import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

interface SessionState {
  sessionId: string;
  messages: Message[];
  completionPercentage: number;
  specSections: Record<string, string>;
  isLoading: boolean;
  selectedRepositories: string[];
  userProfile: 'technical' | 'non_technical';
  
  // Actions
  addMessage: (message: Message) => void;
  updateCompletion: (percentage: number, sections: Record<string, string>) => void;
  setLoading: (loading: boolean) => void;
  setRepositories: (repos: string[]) => void;
  setProfile: (profile: 'technical' | 'non_technical') => void;
  resetSession: () => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  // CORREÇÃO: Gerar sessionId automaticamente
  sessionId: uuidv4(),
  messages: [],
  completionPercentage: 0,
  specSections: {},
  isLoading: false,
  selectedRepositories: [],
  userProfile: 'technical',
  
  addMessage: (message) => 
    set((state) => ({ 
      messages: [...state.messages, message] 
    })),
  
  updateCompletion: (percentage, sections) => 
    set({ 
      completionPercentage: percentage, 
      specSections: sections 
    }),
  
  setLoading: (loading) => 
    set({ isLoading: loading }),
  
  setRepositories: (repos) => 
    set({ selectedRepositories: repos }),
  
  setProfile: (profile) => 
    set({ userProfile: profile }),
  
  resetSession: () => 
    set({
      sessionId: uuidv4(),  // Novo ID
      messages: [],
      completionPercentage: 0,
      specSections: {},
      isLoading: false,
    }),
}));
```

**Instalar uuid se não tiver:**
```bash
cd frontend
npm install uuid
npm install --save-dev @types/uuid
```

---

## 🎯 CORREÇÃO #5: Formato de Mensagens no LangGraph

### Problema
Nodes retornam dict simples mas `add_messages` reducer espera Message objects

### Solução

Atualizar `backend/agent/nodes/core.py`:

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

async def analyze_feature_node(state: AgentState) -> StateUpdate:
    """Analyze feature with proper Message objects"""
    # ... código de análise ...
    
    return {
        "feature_summary": result.get("main_goal", ""),
        "feature_complexity": result.get("complexity", 3),
        "messages": [
            AIMessage(content=f"Entendi! {result.get('main_goal', '')}\n\n...")
        ],
        "current_node": "analyze"
    }

async def llm_response_node(state: AgentState) -> StateUpdate:
    """Generate response with proper Message objects"""
    # ... código LLM ...
    
    return {
        "messages": [
            AIMessage(content=response.choices[0]["message"]["content"])
        ],
        "iteration_count": 1,
        "current_node": "llm_response"
    }
```

**Adicionar ao pyproject.toml:**
```toml
[tool.poetry.dependencies]
langchain-core = "^0.3.0"
```

---

## 🎯 CORREÇÃO #6: Tratamento de Erros no Frontend

### Problema
UI não exibe erros específicos da API

### Solução

Atualizar `frontend/src/components/chat/ChatInterface.tsx`:

```typescript
import { useToast } from '@/components/ui/use-toast';

export default function ChatInterface() {
  const { toast } = useToast();
  
  const handleSend = async () => {
    // ... código existente ...
    
    try {
      const response = await apiClient.chat(
        sessionId, 
        userMessage.content,
        undefined,
        selectedRepositories,
        userProfile
      );
      
      addMessage({
        role: 'assistant',
        content: response.ai_response,
        timestamp: new Date()
      });
      
      updateCompletion(response.completion_percentage, response.spec_sections);
      
    } catch (error) {
      console.error('Chat error:', error);
      
      // CORREÇÃO: Toast com mensagem específica
      toast({
        variant: "destructive",
        title: "Erro na comunicação",
        description: error instanceof Error 
          ? error.message 
          : "Não foi possível enviar a mensagem. Verifique sua conexão.",
      });
      
      addMessage({
        role: 'assistant',
        content: '⚠️ Desculpe, ocorreu um erro. Por favor, tente novamente.',
        timestamp: new Date()
      });
    } finally {
      setLoading(false);
    }
  };
  
  // ... resto do código ...
}
```

---

## 🎯 VALIDAÇÃO FINAL

Depois de aplicar todas as correções:

```bash
# 1. Rebuild completo
cd context-coder
docker-compose down -v
docker-compose build --no-cache
docker-compose up

# 2. Testar endpoints
curl http://localhost:8000/health
# Esperado: {"status": "healthy", ...}

curl http://localhost:8000/api/info
# Esperado: {"features": [...], ...}

# 3. Testar frontend
# Abrir http://localhost:5173
# Verificar:
# - [ ] Chat abre sem erros
# - [ ] Consegue enviar mensagem
# - [ ] Resposta aparece (mesmo que seja erro)
# - [ ] Toast aparece quando há erro
# - [ ] SessionId está presente no DevTools

# 4. Testar MCP (opcional)
curl -X POST http://localhost:8000/api/repositories/discover
# Esperado: lista de repositórios ou erro explicativo
```

---

## ⏭️ PRÓXIMOS PASSOS

Após P0 estar funcional:

1. **Testar fluxo completo end-to-end**
2. **Corrigir P1** (prompts, templates, exportação)
3. **Adicionar testes automatizados**
4. **Documentar setup real** (atualizar README)

---

**Nota:** Essas correções devem ser aplicadas **na ordem apresentada** para máximo de compatibilidade.
