#!/bin/bash
# Setup Environment Variables

echo "🔧 Configurando arquivo .env..."

# Criar .env do backend
cat > backend/.env << 'ENVEOF'
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

echo "✅ Arquivo backend/.env criado!"
echo ""
echo "📝 Próximos passos:"
echo "1. Edite o arquivo backend/.env com suas API keys reais:"
echo "   nano backend/.env"
echo ""
echo "2. Inicie o Docker (se não estiver rodando):"
echo "   sudo systemctl start docker"
echo ""
echo "3. Execute o docker-compose:"
echo "   docker-compose up --build"
echo ""
echo "⚠️  Nota: O frontend foi movido para repositório separado:"
echo "   https://github.com/tperaro/context-coder-front"
