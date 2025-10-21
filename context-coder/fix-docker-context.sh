#!/bin/bash
echo "🔧 Reconfigurando Docker context para usar engine nativo..."

# Remove contexto do Docker Desktop
docker context use default 2>/dev/null || docker context create default --docker "host=unix:///var/run/docker.sock"
docker context use default

# Exporta variável para usar socket correto
export DOCKER_HOST=unix:///var/run/docker.sock

echo "✅ Docker context configurado para engine nativo!"
echo ""
echo "Teste agora:"
echo "docker ps"
