#!/bin/bash
# Context-Coder Backend - Setup Script

echo "🚀 Context-Coder Backend - Setup Rápido"
echo ""

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se .env existe
if [ ! -f backend/.env ]; then
    echo "📝 Criando arquivo backend/.env..."
    cp backend/.env.example backend/.env
    echo "⚠️  IMPORTANTE: Edite o arquivo backend/.env com suas API keys reais!"
    echo "   nano backend/.env"
    echo ""
    read -p "Pressione Enter depois de configurar o backend/.env..."
fi

echo "✅ Configuração completa!"
echo ""
echo "🐳 Iniciando backend com Docker..."
echo ""

# Iniciar Docker Compose
docker-compose up --build

echo ""
echo "🎉 Backend rodando!"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
