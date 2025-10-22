# Context-Coder Backend

API backend para o Context-Coder - Plataforma AI-powered que transforma contexto de repositórios em especificações técnicas acionáveis.

## 🚀 Stack Tecnológica

- **FastAPI 0.116.1+** - Framework web moderno e async
- **LangGraph 0.6.0** - Orquestração de agentes com checkpointing
- **Gemini 2.5 Pro** - LLM via Google Direct API + OpenRouter fallback
- **LangSmith** - Observabilidade e debugging de agentes (opcional)
- **Model Context Protocol (MCP)** - Busca semântica no código usando `zilliztech/claude-context`
- **Python 3.11+** - Linguagem base
- **Poetry** - Gerenciamento de dependências
- **Docker** - Containerização

## ⚡ Quick Start

### Pré-requisitos

- Docker & Docker Compose **OU**
- Python 3.11+ com Poetry
- **API Keys necessárias:**
  - OpenRouter (para Gemini 2.5 Pro)
  - OpenAI (para embeddings do MCP)
  - Zilliz Cloud (vector storage)

### Opção 1: Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/tperaro/context-coder.git
cd context-coder

# 2. Setup automático (cria .env e inicia)
./setup.sh

# OU manualmente:
cp backend/.env.example backend/.env
# Edite backend/.env com suas API keys
docker-compose up --build

# ✅ Acesse:
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Opção 2: Local (Desenvolvimento)

```bash
# 1. Entre na pasta backend
cd backend

# 2. Instale dependências
poetry install

# 3. Configure ambiente
cp .env.example .env
# Edite .env com suas API keys

# 4. Ative o ambiente virtual
poetry shell

# 5. Inicie o servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# ✅ Acesse: http://localhost:8000/docs
```

## 📁 Estrutura do Projeto

```
context-coder/
├── backend/                 # Código-fonte do backend
│   ├── agent/              # LangGraph agent
│   │   ├── state.py        # AgentState TypedDict
│   │   ├── graph.py        # Construção do grafo
│   │   ├── nodes/          # Nós do grafo
│   │   ├── edges.py        # Lógica de roteamento
│   │   ├── checkpointing.py # SessionManager
│   │   └── prompts/        # Templates de prompts
│   ├── api/                # Endpoints FastAPI
│   │   ├── agent.py
│   │   ├── export.py
│   │   ├── github.py
│   │   └── repositories.py
│   ├── services/           # Serviços externos
│   │   ├── llm.py          # OpenRouter/Gemini
│   │   ├── mcp.py          # MCP integration
│   │   ├── export.py
│   │   └── github.py
│   ├── tests/              # Testes
│   ├── main.py             # Entry point
│   ├── pyproject.toml      # Poetry deps
│   ├── .env.example        # Template de config
│   └── Dockerfile
├── docs/                   # Documentação
│   ├── QUICKSTART.md
│   ├── RUN_WITHOUT_DOCKER.md
│   └── FRONTEND_MOVED.md
├── scripts/                # Scripts auxiliares
│   ├── setup-env.sh
│   ├── start.sh
│   └── fix-docker-context.sh
├── specs/                  # Especificações técnicas
├── docker-compose.yml      # Orquestração Docker
├── Makefile                # Comandos úteis
├── setup.sh                # Setup rápido
└── README.md               # Este arquivo
```

## 🌐 Variáveis de Ambiente

Copie `backend/.env.example` para `backend/.env` e configure:

```bash
# Google Gemini (Primary LLM)
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_MODEL=gemini-1.5-flash

# OpenRouter (Fallback LLM)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=google/gemini-flash-1.5

# OpenAI (Embeddings for MCP)
OPENAI_API_KEY=sk-your-openai-key-here

# Zilliz Cloud (Vector DB for MCP)
ZILLIZ_CLOUD_URI=https://your-instance.zilliz.cloud
ZILLIZ_CLOUD_API_KEY=your-zilliz-key-here

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173

# LangSmith (Optional - Observability)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=lsv2_pt_your-key-here
LANGCHAIN_PROJECT=context-coder-dev

# GitHub (Optional)
GITHUB_TOKEN=
GITHUB_ORG=your-org
GITHUB_PROJECT_NUMBER=1
```

**Onde conseguir as keys:**
- Google Gemini: https://aistudio.google.com/apikey (FREE)
- OpenRouter: https://openrouter.ai/keys
- OpenAI: https://platform.openai.com/api-keys
- Zilliz Cloud: https://cloud.zilliz.com/signup (FREE tier)
- **LangSmith: https://smith.langchain.com/ (FREE - opcional)** 🆕

## 🔧 Comandos Úteis (Makefile)

```bash
make help          # Ver todos os comandos
make install       # Instalar dependências
make build         # Build Docker image
make up            # Iniciar serviços
make up-d          # Iniciar em background
make down          # Parar serviços
make logs          # Ver logs
make logs-backend  # Logs do backend
make test          # Executar testes
make shell-backend # Shell no container
make clean         # Limpar containers
```

## 🧪 Testes

```bash
# Com Docker
make test

# Ou localmente
cd backend
poetry run pytest
poetry run pytest tests/integration/ -v
poetry run pytest --cov=. --cov-report=html
```

## 📡 API Endpoints

A API está documentada interativamente em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Principais endpoints:

- `POST /api/agent/invoke` - Enviar mensagem ao agente
- `POST /api/agent/stream` - Chat com streaming (SSE)
- `GET /api/repositories` - Listar repositórios
- `POST /api/export/markdown` - Exportar especificação
- `POST /api/github/create-card` - Criar card no GitHub Projects

## 📊 LangSmith - Observabilidade (Opcional)

O backend está integrado com o **LangSmith** para rastreamento e debugging de agentes! 

### Setup Rápido (5 minutos)

1. Obtenha uma API key gratuita em [smith.langchain.com](https://smith.langchain.com/)
2. Adicione ao seu `backend/.env`:
   ```bash
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=lsv2_pt_sua_chave_aqui
   LANGCHAIN_PROJECT=context-coder-dev
   ```
3. Reinicie o backend
4. Acesse [smith.langchain.com](https://smith.langchain.com/) para ver traces em tempo real!

### O que você ganha?

- 🔍 **Rastreamento completo** de todas as execuções do agent
- 🐛 **Debug visual** do fluxo de nodes (analyze → search → llm → update)
- 📈 **Métricas** de performance, latência e custos
- 🏷️ **Tags** para organizar traces: `agent`, `analysis`, `tech-debt`, etc
- 🔗 **Visualização** de prompts, respostas e decisões da IA

### Nodes rastreados

Todos os nodes principais estão instrumentados:
- ✅ `analyze_feature` - Análise inicial
- ✅ `search_codebase` - Busca via MCP
- ✅ `llm_response` - Geração de resposta
- ✅ `tech_debt_analysis` - Análise de dívida técnica
- ✅ `security_check` - Checklist de segurança
- ✅ `generate_diagram` - Geração de diagramas

📖 **Documentação completa**: [docs/LANGSMITH_INTEGRATION.md](./docs/LANGSMITH_INTEGRATION.md)

## 🎯 Frontend

O frontend foi movido para repositório separado:

📦 **[context-coder-front](https://github.com/tperaro/context-coder-front)**

Para usar a aplicação completa, você precisa:
1. Rodar este backend
2. Rodar o frontend (repositório separado)

## 🐛 Troubleshooting

### Erro: "API key not found"

Verifique se o arquivo `backend/.env` existe e contém todas as keys necessárias.

```bash
# Verificar se .env existe
ls -la backend/.env

# Copiar do exemplo se necessário
cp backend/.env.example backend/.env
```

### Erro: "Port 8000 already in use"

```bash
# Matar processo na porta
lsof -ti:8000 | xargs kill -9

# Ou usar outra porta
uvicorn main:app --port 8001
```

### Erro: CORS

Certifique-se de que `CORS_ORIGINS` no `backend/.env` inclui a URL do frontend:

```bash
CORS_ORIGINS=http://localhost:5173
```

## 📚 Documentação Adicional

- [QUICKSTART.md](./docs/QUICKSTART.md) - Guia rápido completo
- [LANGSMITH_INTEGRATION.md](./docs/LANGSMITH_INTEGRATION.md) - Observabilidade com LangSmith 🆕
- [RUN_WITHOUT_DOCKER.md](./docs/RUN_WITHOUT_DOCKER.md) - Rodar sem Docker
- [FRONTEND_MOVED.md](./docs/FRONTEND_MOVED.md) - Info sobre separação do frontend
- [Especificações](./specs/) - Specs técnicas do projeto

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add: nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

[Especificar licença]

---

**Desenvolvido com ❤️ usando FastAPI, LangGraph e Gemini 2.5 Pro**
