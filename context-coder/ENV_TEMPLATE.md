# Environment Variables Template

## 📁 Arquivo Principal: `.env` (raiz do projeto)

```bash
# ============================================
# Context2Task - Environment Variables
# ============================================

# ============================================
# REQUIRED - OpenRouter API (for Gemini 2.5 Pro)
# ============================================
# Get your key at: https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-your-key-here
DEFAULT_MODEL=google/gemini-2.5-pro

# ============================================
# REQUIRED - OpenAI API (for MCP Embeddings)
# ============================================
# Get your key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-key-here

# ============================================
# REQUIRED - Zilliz Cloud (MCP Vector Storage)
# ============================================
# Get free tier at: https://cloud.zilliz.com/signup
ZILLIZ_CLOUD_URI=https://your-instance.zilliz.cloud
ZILLIZ_CLOUD_API_KEY=your-zilliz-api-key-here

# ============================================
# APPLICATION SETTINGS
# ============================================
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173

# ============================================
# OPTIONAL - GitHub Projects Integration
# ============================================
GITHUB_TOKEN=
GITHUB_ORG=your-organization
GITHUB_PROJECT_NUMBER=1
```

## 📁 Frontend: `frontend/.env`

```bash
VITE_API_URL=http://localhost:8000
```

## 📁 Backend: `backend/.env`

```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
DEFAULT_MODEL=google/gemini-2.5-pro
OPENAI_API_KEY=sk-your-openai-key-here
ZILLIZ_CLOUD_URI=https://your-instance.zilliz.cloud
ZILLIZ_CLOUD_API_KEY=your-zilliz-api-key-here
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
GITHUB_TOKEN=
GITHUB_ORG=your-organization
GITHUB_PROJECT_NUMBER=1
```

## 🚀 Quick Setup

```bash
# 1. Criar arquivo principal .env
cat > .env << 'ENVEOF'
OPENROUTER_API_KEY=your-key-here
DEFAULT_MODEL=google/gemini-2.5-pro
OPENAI_API_KEY=your-key-here
ZILLIZ_CLOUD_URI=https://your-instance.zilliz.cloud
ZILLIZ_CLOUD_API_KEY=your-key-here
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
GITHUB_TOKEN=
GITHUB_ORG=your-org
GITHUB_PROJECT_NUMBER=1
ENVEOF

# 2. Editar com suas keys reais
nano .env

# 3. Copiar para frontend
echo "VITE_API_URL=http://localhost:8000" > frontend/.env

# 4. Copiar para backend
cp .env backend/.env

# 5. Iniciar!
docker-compose up --build
```

## 🔑 Onde Conseguir as Keys

1. **OpenRouter**: https://openrouter.ai/keys
   - Cadastre-se grátis
   - Crie uma API key
   - Adicione créditos ($5 = ~500 conversas)

2. **OpenAI**: https://platform.openai.com/api-keys
   - Necessário para embeddings do MCP
   - Custo mínimo (~$0.01/mês)

3. **Zilliz Cloud**: https://cloud.zilliz.com/
   - Free tier: 2M vectors
   - Suficiente para MVP
   - Crie cluster e copie URI + API Key

4. **GitHub Token** (opcional): https://github.com/settings/tokens
   - Scopes: repo, project
   - Apenas se quiser integração com GitHub Projects

## ⚠️ Segurança

- ❌ NUNCA commite `.env` para git
- ✅ `.env` já está no `.gitignore`
- ✅ Use keys diferentes para dev/prod
- ✅ Rotacione keys periodicamente

## 💰 Estimativa de Custos (MVP)

- OpenRouter: ~$2-5/mês (50 specs)
- OpenAI: ~$0.01/mês (embeddings)
- Zilliz: $0 (free tier)
- **Total: ~$5/mês**
