#!/bin/bash
# Setup Environment Variables

echo "🔧 Configurando arquivos .env..."

# 1. Criar .env principal (RAIZ - docker-compose lê daqui)
cat > .env << 'ENVEOF'
# OpenRouter (LLM)
OPENROUTER_API_KEY=sk-or-v1-SEU-KEY-AQUI
DEFAULT_MODEL=google/gemini-2.5-pro

# OpenAI (MCP Embeddings)
OPENAI_API_KEY=sk-SEU-KEY-AQUI

# Zilliz Cloud (Vector DB)
ZILLIZ_CLOUD_URI=https://SEU-CLUSTER.zilliz.cloud
ZILLIZ_CLOUD_API_KEY=SEU-KEY-AQUI

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173

# GitHub (opcional)
GITHUB_TOKEN=
GITHUB_ORG=your-org
GITHUB_PROJECT_NUMBER=1
ENVEOF

# 2. Criar .env do frontend (apenas API URL)
cat > frontend/.env << 'FEEOF'
VITE_API_URL=http://localhost:8000
FEEOF

# 3. Backend herda via docker-compose, mas pode criar por segurança
cp .env backend/.env

echo "✅ Arquivos .env criados!"
echo ""
echo "📝 Próximos passos:"
echo "1. Edite o arquivo .env na RAIZ com suas API keys reais:"
echo "   nano .env"
echo ""
echo "2. Inicie o Docker (se não estiver rodando):"
echo "   sudo systemctl start docker"
echo ""
echo "3. Execute o docker-compose:"
echo "   docker-compose up --build"
