# 🚀 Como Rodar SEM Docker

## 📋 Pré-requisitos

### 1. Python 3.11+
```bash
python3 --version  # Deve ser 3.11+
```

### 2. Node.js 20+
```bash
node --version  # Deve ser 20+
```

### 3. Poetry (gerenciador Python)
```bash
curl -sSL https://install.python-poetry.org | python3 -
# Ou
pip install poetry==1.7.1
```

---

## 🔧 Setup Inicial

### 1. Clone e navegue
```bash
cd /home/peras/gitperaro/context-coder/context-coder
```

### 2. Configure variáveis de ambiente
```bash
# Criar .env na raiz
cp ENV_TEMPLATE.md .env
nano .env  # Edite com suas API keys

# Criar .env no frontend
echo "VITE_API_URL=http://localhost:8000" > frontend/.env

# Copiar para backend
cp .env backend/.env
```

---

## 🐍 Backend (Python + FastAPI)

### Terminal 1 - Backend

```bash
# Entre na pasta backend
cd backend

# Instale dependências
poetry install

# Ative o ambiente virtual
poetry shell

# Ou execute direto com poetry run
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend rodando em:** http://localhost:8000

**API Docs:** http://localhost:8000/docs

---

## ⚛️ Frontend (React + Vite)

### Terminal 2 - Frontend

```bash
# Entre na pasta frontend
cd frontend

# Instale dependências
npm install

# Inicie o dev server
npm run dev
```

**Frontend rodando em:** http://localhost:5173

---

## 📝 Resumo dos Comandos

### Backend
```bash
cd backend
poetry install           # Instala dependências (1x)
poetry shell            # Ativa venv
uvicorn main:app --reload  # Inicia server

# OU direto:
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install             # Instala dependências (1x)
npm run dev            # Inicia dev server
```

---

## 🧪 Rodando Testes

### Backend Tests
```bash
cd backend
poetry run pytest                      # Todos os testes
poetry run pytest tests/integration/   # Só integração
poetry run pytest --cov=.              # Com coverage
```

### Frontend Tests (se tiver)
```bash
cd frontend
npm test
```

---

## 🔍 Troubleshooting

### Erro: "Poetry não encontrado"
```bash
# Adicione ao PATH
export PATH="$HOME/.local/bin:$PATH"
# Adicione ao ~/.bashrc para persistir
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Erro: "Module not found"
```bash
# Backend
cd backend
poetry install --no-root

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Erro: "Port already in use"
```bash
# Backend (porta 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (porta 5173)
lsof -ti:5173 | xargs kill -9
```

### Erro: API keys não carregadas
```bash
# Verifique se .env existe
ls -la backend/.env

# Exporte manualmente (temporário)
export OPENROUTER_API_KEY=sua-key
export OPENAI_API_KEY=sua-key
export ZILLIZ_CLOUD_URI=seu-uri
export ZILLIZ_CLOUD_API_KEY=sua-key

# Depois execute
cd backend
poetry run uvicorn main:app --reload
```

---

## 🎯 Workflow Diário

### Modo Desenvolvimento Normal

**Terminal 1 (Backend):**
```bash
cd backend
poetry shell
uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

**Terminal 3 (Testes/Comandos):**
```bash
# Aqui você roda testes, git, etc
poetry run pytest
```

---

## 📦 Estrutura de Dependências

### Backend (pyproject.toml)
- FastAPI 0.116.1+
- LangGraph 0.6.0
- httpx (OpenRouter)
- pydantic 2.5+

### Frontend (package.json)
- React 18
- Vite 5
- TypeScript
- Zustand (state)
- shadcn/ui

---

## 🔄 Atualizar Dependências

### Backend
```bash
cd backend
poetry update           # Atualiza todas
poetry add package@^1.0 # Adiciona nova
poetry remove package   # Remove
```

### Frontend
```bash
cd frontend
npm update              # Atualiza todas
npm install package@^1.0 # Adiciona nova
npm uninstall package   # Remove
```

---

## 🚀 Build para Produção

### Backend
```bash
cd backend
poetry export -f requirements.txt --output requirements.txt
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
cd frontend
npm run build
# Saída em: frontend/dist/

# Servir com servidor estático
npm install -g serve
serve -s dist -l 3000
```

---

## 💡 Dicas Pro

### 1. Hot Reload mais rápido
```bash
# Backend: Watchfiles é mais rápido que watchgod
poetry add watchfiles

# Frontend: já usa Vite (super rápido)
```

### 2. Debug no VSCode
Crie `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend",
      "env": {"PYTHONPATH": "${workspaceFolder}/backend"}
    }
  ]
}
```

### 3. Aliases úteis (~/.bashrc)
```bash
alias c2t-backend="cd ~/gitperaro/context-coder/context-coder/backend && poetry run uvicorn main:app --reload"
alias c2t-frontend="cd ~/gitperaro/context-coder/context-coder/frontend && npm run dev"
alias c2t-test="cd ~/gitperaro/context-coder/context-coder/backend && poetry run pytest"
```

---

## 🐛 Debug Comum

### Backend não conecta no MCP
```bash
# Verifique se Node.js está instalado
node --version

# MCP usa npx, teste:
npx @zilliztech/claude-context --version
```

### Frontend não conecta no Backend
```bash
# Verifique CORS no backend/main.py
# Verifique VITE_API_URL no frontend/.env
cat frontend/.env
```

---

## ✅ Checklist de Setup

- [ ] Python 3.11+ instalado
- [ ] Node.js 20+ instalado
- [ ] Poetry instalado
- [ ] `.env` configurado (raiz, backend/, frontend/)
- [ ] API keys válidas
- [ ] Backend rodando (porta 8000)
- [ ] Frontend rodando (porta 5173)
- [ ] http://localhost:5173 acessível

---

**🎉 Pronto! Agora você pode desenvolver sem Docker!**

**Vantagens:**
- ✅ Hot reload mais rápido
- ✅ Debug direto no VSCode
- ✅ Não precisa rebuild de containers
- ✅ Usa menos memória RAM

**Desvantagens:**
- ❌ Precisa instalar dependências localmente
- ❌ Pode ter conflitos de versões
- ❌ Setup inicial mais trabalhoso
