# Context2Task - AI-Powered Feature Specification Platform

Plataforma que transforma contexto de repositórios em tasks acionáveis usando IA.

## 🚀 Quick Start (1 comando!)

```bash
# 1. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas API keys

# 2. Suba tudo com Docker Compose
docker-compose up --build

# 3. Acesse
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 📋 Pré-requisitos

- Docker & Docker Compose
- **API Keys** necessárias:
  - OpenRouter API key (para Gemini 2.5 Pro)
  - OpenAI API key (para embeddings do MCP)
  - Zilliz Cloud URI + API key (para vector storage)

## 🏗️ Arquitetura

```
context-coder/
├── frontend/          # React + Vite + TypeScript + shadcn/ui
├── backend/           # FastAPI + LangGraph + Gemini 2.5 Pro
├── docker-compose.yml # Orquestração completa
└── .env               # Configuração (não commitado)
```

### Stack Tecnológica

**Frontend:**
- React 18 + TypeScript
- Vite (dev server rápido)
- shadcn/ui (Radix UI + Tailwind CSS)
- Zustand (state management)

**Backend:**
- FastAPI 0.116.1+ (async endpoints)
- LangGraph 0.6.0 (agent orchestration)
- Gemini 2.5 Pro via OpenRouter
- Model Context Protocol (MCP) - `zilliztech/claude-context`

**Infrastructure:**
- Docker + Docker Compose
- Hot-reload para desenvolvimento
- CORS configurado

## 🔧 Desenvolvimento

### Comandos Úteis

```bash
# Iniciar serviços
docker-compose up

# Rebuild após mudanças no Dockerfile
docker-compose up --build

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Parar serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

### Estrutura de Pastas

```
backend/
├── agent/
│   ├── state.py           # AgentState TypedDict
│   ├── graph.py           # LangGraph construction
│   ├── nodes/             # Graph nodes
│   │   ├── core.py        # Core nodes
│   │   ├── tech_debt.py
│   │   ├── security.py
│   │   └── diagram.py
│   ├── edges.py           # Routing logic
│   ├── checkpointing.py   # SessionManager
│   └── prompts/           # Prompt templates
│       └── profiles.py
├── services/
│   ├── llm.py             # OpenRouter/Gemini service
│   └── mcp.py             # MCP integration
├── api/
│   └── agent.py           # FastAPI endpoints
├── main.py                # App entry point
└── pyproject.toml         # Poetry dependencies

frontend/
├── src/
│   ├── components/
│   │   ├── ui/            # shadcn components
│   │   ├── chat/          # Chat interface
│   │   ├── sidebar/       # Sidebar com dropdowns
│   │   └── preview/       # Markdown preview modal
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Session.tsx
│   │   └── Review.tsx
│   ├── stores/
│   │   └── session.ts
│   └── api/
│       └── client.ts
├── package.json
└── vite.config.ts
```

## 📝 Variáveis de Ambiente

Veja `.env.example` para todas as variáveis necessárias.

**Críticas:**
- `OPENROUTER_API_KEY` - Acesso ao Gemini 2.5 Pro
- `OPENAI_API_KEY` - Para embeddings do MCP
- `ZILLIZ_CLOUD_URI` - Vector database
- `ZILLIZ_CLOUD_API_KEY` - Auth para Zilliz

## 🧪 Testing

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test

# Integration tests
docker-compose exec backend pytest tests/integration/
```

## 📚 Documentação

- **Especificação Completa**: `specs/active/ai-feature-assistant-platform/spec.md`
- **Plano Técnico**: `specs/active/ai-feature-assistant-platform/plan.md`
- **Tasks Detalhadas**: `specs/active/ai-feature-assistant-platform/tasks.md`
- **API Docs (auto-geradas)**: http://localhost:8000/docs

## 🔐 Segurança

⚠️ **IMPORTANTE**: Nunca commite `.env` com API keys reais!

- Use `.env.example` como template
- API keys devem estar em `.env` (gitignored)
- Para produção, use secrets management (AWS Secrets Manager, etc.)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

## 📄 Licença

[Especificar licença]

## 🙋 Suporte

- Issues: [GitHub Issues]
- Documentação: `specs/` folder
- Contact: [Especificar]

---

**Desenvolvido com ❤️ usando FastAPI, React, LangGraph e Gemini 2.5 Pro**


