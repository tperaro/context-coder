# Context-Coder Backend

API backend para o Context-Coder - Plataforma AI-powered que transforma contexto de repositórios em especificações técnicas acionáveis.

## 🚀 Stack Tecnológica

- **FastAPI 0.116.1+** - Framework web moderno e async
- **LangGraph 0.6.0** - Orquestração de agentes com checkpointing
- **Gemini 2.5 Pro** - LLM via OpenRouter
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
# OpenRouter (LLM)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
DEFAULT_MODEL=google/gemini-2.5-pro

# OpenAI (Embeddings)
OPENAI_API_KEY=sk-your-openai-key-here

# Zilliz Cloud (Vector DB)
ZILLIZ_CLOUD_URI=https://your-instance.zilliz.cloud
ZILLIZ_CLOUD_API_KEY=your-zilliz-key-here

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173

# GitHub (opcional)
GITHUB_TOKEN=
GITHUB_ORG=your-org
GITHUB_PROJECT_NUMBER=1
```

**Onde conseguir as keys:**
- OpenRouter: https://openrouter.ai/keys
- OpenAI: https://platform.openai.com/api-keys
- Zilliz Cloud: https://cloud.zilliz.com/signup

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
