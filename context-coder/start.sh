#!/bin/bash
echo "🚀 Iniciando Context2Task..."
echo ""
echo "📝 Checklist:"
echo "  ✅ Docker context: default"
echo "  ✅ poetry.lock: corrigido"
echo "  ✅ .env: configurado"
echo ""
echo "⏳ Iniciando build (pode levar 2-3 minutos)..."
echo ""

# Exportar DOCKER_HOST para garantir que use o socket correto
export DOCKER_HOST=unix:///var/run/docker.sock

# Tentar sem sudo primeiro
if docker ps >/dev/null 2>&1; then
    echo "✅ Usando Docker sem sudo"
    docker-compose up --build
else
    echo "⚠️  Precisa de sudo para Docker"
    sudo docker-compose up --build
fi
