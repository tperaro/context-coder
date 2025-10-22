# Context-Coder Backend - Makefile

.PHONY: help build up down logs test clean install

help: ## Mostrar esta mensagem de ajuda
	@echo "Context-Coder Backend - Comandos Disponíveis"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependências
	@echo "📦 Instalando dependências do backend..."
	cd backend && poetry install
	@echo "✅ Dependências instaladas!"
	@echo ""
	@echo "⚠️  Não esqueça de configurar o backend/.env:"
	@echo "   cp backend/.env.example backend/.env"
	@echo "   nano backend/.env"

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up

up-d: ## Start all services in background
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Follow logs
	docker-compose logs -f

logs-backend: ## Follow backend logs only
	docker-compose logs -f backend

test: ## Run backend tests
	docker-compose exec backend pytest

test-integration: ## Run integration tests only
	docker-compose exec backend pytest tests/integration/ -v

test-coverage: ## Run tests with coverage
	docker-compose exec backend pytest --cov=. --cov-report=html

clean: ## Clean Docker containers and volumes
	docker-compose down -v
	docker system prune -f

restart: ## Restart all services
	docker-compose restart

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

format: ## Format backend code
	docker-compose exec backend black .
	docker-compose exec backend ruff --fix .

check: ## Check code quality
	docker-compose exec backend black --check .
	docker-compose exec backend ruff .


