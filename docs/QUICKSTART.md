# Context2Task - Quick Start Guide 🚀

## 🎯 O que é Context2Task?

Plataforma AI-powered que transforma o contexto do seu repositório em especificações técnicas detalhadas usando:
- **LangGraph**: Orquestração de agentes com checkpointing
- **Gemini 2.5 Pro**: LLM via OpenRouter
- **MCP (Model Context Protocol)**: Busca semântica no código
- **React + FastAPI**: Interface moderna e API performática

---

## ⚡ Início Rápido (3 passos)

### 1. Clone e Configure

```bash
git clone <repo-url>
cd context-coder/context-coder

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas API keys
```

### 2. Inicie com Docker Compose

```bash
# Opção 1: Comando único
docker-compose up --build

# Opção 2: Usando Makefile
make build
make up
```

### 3. Acesse

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Nota:** O frontend foi movido para repositório separado:  
👉 [context-coder-front](https://github.com/tperaro/context-coder-front)

---

## 🔑 Variáveis de Ambiente Necessárias

Edite `.env` com:

```bash
# OpenRouter (para Gemini 2.5 Pro)
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# OpenAI (para embeddings do MCP)
OPENAI_API_KEY=sk-xxxxx

# Zilliz Cloud (vector database do MCP)
ZILLIZ_CLOUD_URI=https://your-instance.zilliz.cloud
ZILLIZ_CLOUD_API_KEY=xxxxx

# Opcional: GitHub Projects
GITHUB_TOKEN=ghp_xxxxx
GITHUB_ORG=your-org
GITHUB_PROJECT_NUMBER=1
```

**Onde conseguir:**
- OpenRouter: https://openrouter.ai/
- OpenAI: https://platform.openai.com/
- Zilliz Cloud: https://cloud.zilliz.com/

---

## 📖 Como Usar

### 1. Criar Nova Especificação

**Nota:** Primeiro configure e execute o frontend (repositório separado).

1. Clone e execute o [frontend](https://github.com/tperaro/context-coder-front)
2. Acesse http://localhost:5173
3. Clique em "🚀 Criar Nova Especificação"
4. Selecione seu perfil (Técnico ou Negócio)
5. Adicione repositórios para análise
6. Descreva a feature no chat

### 2. Conversa Interativa

O agente vai:
- Fazer perguntas clarificadoras
- Buscar contexto relevante no código
- Preencher progressivamente as 10 seções da spec

### 3. Features Adicionais (quando ≥ 80%)

- **Tech Debt**: Análise AI de dívida técnica
- **Segurança**: Checklist LGPD + OWASP
- **Diagrama**: Geração de Mermaid diagram
- **Multi-Spec**: Divisão automática para múltiplos repos

### 4. Exportar

- **Markdown**: Download do `.md` completo
- **GitHub Projects**: Criar card no backlog

---

## 🧪 Testar

```bash
# Testes unitários
docker-compose exec backend pytest

# Testes de integração
docker-compose exec backend pytest tests/integration/ -v

# Com coverage
docker-compose exec backend pytest --cov=.

# Ou usando Makefile
make test
make test-integration
```

---

## 🛠️ Comandos Úteis

```bash
# Ver logs em tempo real
docker-compose logs -f

# Logs apenas do backend
docker-compose logs -f backend

# Parar serviços
docker-compose down

# Rebuild completo
docker-compose down -v && docker-compose up --build

# Acessar shell do backend
docker-compose exec backend /bin/bash

# Ou usando Makefile
make logs
make down
make shell-backend
```

---

## 📁 Estrutura do Projeto

```
context-coder/
├── backend/               # FastAPI + LangGraph
│   ├── agent/            # LangGraph agent
│   │   ├── state.py      # AgentState TypedDict
│   │   ├── graph.py      # Graph construction
│   │   ├── nodes/        # Graph nodes
│   │   │   ├── core.py   # Main conversation loop
│   │   │   └── optional.py # Tech debt, security, etc.
│   │   ├── edges.py      # Routing logic
│   │   ├── checkpointing.py # SessionManager
│   │   └── prompts/      # Prompt templates
│   │       └── profiles.py # Technical/Non-technical
│   ├── services/         # External integrations
│   │   ├── llm.py        # OpenRouter/Gemini
│   │   ├── mcp.py        # Model Context Protocol
│   │   ├── export.py     # Markdown export
│   │   └── github.py     # GitHub Projects
│   ├── api/              # FastAPI endpoints
│   │   ├── agent.py      # Chat & commands
│   │   ├── export.py     # Export endpoints
│   │   └── github.py     # GitHub integration
│   ├── main.py           # FastAPI app
│   └── pyproject.toml    # Poetry dependencies
│
├── docker-compose.yml    # Orquestração
├── .env.example          # Template de variáveis
├── Makefile              # Comandos úteis
└── README.md             # Documentação completa
```

---

## 🎓 Conceitos Chave

### LangGraph Agent

```python
# O agente segue este fluxo:
START → analyze → search → llm_response → update_spec → check_completion
                                                          ↓
                                                     wait_input (interrupt)
                                                          ↓
                                          [user command routing]
                                                          ↓
                    tech_debt | security | diagram | multi_spec | continue | export
```

### Checkpointing

Cada sessão é persistida automaticamente:
- Estado completo salvo após cada nó
- Pode retomar conversas
- Suporta múltiplas sessões concorrentes

### Prompts Adaptáveis

Dois perfis de usuário:
- **Technical**: Linguagem técnica, detalhes de implementação
- **Non-technical**: Linguagem simples, foco em valor de negócio

---

## ❓ Troubleshooting

### Backend não inicia

```bash
# Verificar logs
docker-compose logs backend

# Problema comum: API keys não configuradas
# Solução: Editar .env com keys válidas
```

### Frontend não conecta ao backend

**Nota:** O frontend está em repositório separado: [context-coder-front](https://github.com/tperaro/context-coder-front)

```bash
# Verificar se backend está rodando
curl http://localhost:8000/health

# Backend deve permitir CORS para localhost:5173
# Verifique no .env:
CORS_ORIGINS=http://localhost:5173
```

### MCP não funciona

```bash
# Verificar Node.js no container
docker-compose exec backend node --version

# Verificar variáveis do Zilliz Cloud
echo $ZILLIZ_CLOUD_URI
echo $ZILLIZ_CLOUD_API_KEY
```

---

## 🚀 Próximos Passos

1. **Indexar seus repositórios**:
   ```bash
   # Via MCP CLI (dentro do container)
   npx @zilliztech/claude-context index-codebase /path/to/repo
   ```

2. **Personalizar prompts**: Edite `backend/agent/prompts/profiles.py`

3. **Adicionar regras de segurança**: Customize `backend/agent/nodes/optional.py`

4. **Integrar com GitHub**: Configure `GITHUB_TOKEN` no `.env`

---

## 📚 Documentação Completa

- **README.md**: Arquitetura e visão geral
- **API Docs**: http://localhost:8000/docs (após iniciar)
- **Specs**: Ver pasta `specs/active/ai-feature-assistant-platform/`

---

## 💡 Dica Pro

Use o Makefile para comandos rápidos:

```bash
make help          # Ver todos os comandos
make up            # Iniciar
make logs          # Ver logs
make test          # Rodar testes
make shell-backend # Acessar backend
```

---

**Desenvolvido com ❤️ usando FastAPI, React, LangGraph e Gemini 2.5 Pro**


