# Pulso-AI Makefile
# Automation for common development tasks

.PHONY: help install install-dev setup-dev clean lint test test-quick test-cov docker-up docker-down docs

# Default target
help: ## Show this help message
	@echo "Pulso-AI Development Commands"
	@echo "=============================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation and Setup
install: ## Install production dependencies
	cd core-template && pip install -r requirements/base.txt

install-dev: ## Install development dependencies
	cd core-template && pip install -r requirements/dev.txt
	pre-commit install

setup-dev: ## Complete development environment setup
	@echo "🚀 Setting up Pulso-AI development environment..."
	make install-dev
	make docker-up
	@echo "✅ Development environment ready!"
	@echo "📝 Next steps:"
	@echo "   - Run 'make test' to verify setup"
	@echo "   - Check services: http://localhost:5050 (pgAdmin), http://localhost:8081 (Redis)"

# Code Quality
lint: ## Run all linting tools
	@echo "🔍 Running linting tools..."
	cd core-template && black --check src/
	cd core-template && isort --check-only src/
	cd core-template && flake8 src/
	cd core-template && mypy src/
	cd core-template && bandit -r src/

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	cd core-template && black src/
	cd core-template && isort src/

# Testing
test: ## Run all tests with coverage
	@echo "🧪 Running tests with coverage..."
	cd core-template && pytest -v --cov=src --cov-report=term-missing

test-quick: ## Run tests without coverage (faster)
	@echo "⚡ Running quick tests..."
	cd core-template && pytest -v -x --tb=short

test-unit: ## Run only unit tests
	cd core-template && pytest -v -m "unit"

test-integration: ## Run only integration tests
	cd core-template && pytest -v -m "integration"

test-cov: ## Generate detailed coverage report
	cd core-template && pytest --cov=src --cov-report=html
	@echo "📊 Coverage report: core-template/htmlcov/index.html"

# Docker Services
docker-up: ## Start development services (PostgreSQL, Redis)
	@echo "🐳 Starting development services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "   - PostgreSQL: localhost:5432"
	@echo "   - Redis: localhost:6379" 
	@echo "   - pgAdmin: http://localhost:5050"
	@echo "   - Redis Commander: http://localhost:8081"

docker-down: ## Stop development services
	@echo "🛑 Stopping development services..."
	docker-compose down

docker-logs: ## View docker services logs
	docker-compose logs -f

docker-clean: ## Clean docker volumes and containers
	docker-compose down -v --remove-orphans
	docker system prune -f

# Development Server
dev: ## Start development server
	cd core-template && uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

dev-debug: ## Start development server with debugging
	cd core-template && python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn src.api.main:app --reload

# Frontend (when available)
frontend-install: ## Install frontend dependencies
	cd frontend && npm install

frontend-dev: ## Start frontend development server
	cd frontend && npm run dev

frontend-build: ## Build frontend for production
	cd frontend && npm run build

frontend-test: ## Run frontend tests
	cd frontend && npm test

# Utilities
clean: ## Clean cache and temporary files
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

check: ## Run all checks (lint + test)
	make lint
	make test

docs: ## Generate documentation
	cd core-template && mkdocs serve

docs-build: ## Build documentation
	cd core-template && mkdocs build

# Client Management (scripts)
create-client: ## Create new client (usage: make create-client CLIENT=client-name)
	python scripts/client-management/create_client.py $(CLIENT)

deploy-client: ## Deploy client (usage: make deploy-client CLIENT=client-name ENV=dev)
	python scripts/client-management/deploy_client.py $(CLIENT) --env $(ENV)

# Database
db-init: ## Initialize development databases
	@echo "🗄️ Initializing databases..."
	# This will be implemented when we have database initialization scripts

db-migrate: ## Run database migrations
	@echo "🔄 Running migrations..."
	# This will be implemented with alembic

db-seed: ## Seed database with test data
	@echo "🌱 Seeding test data..."
	# This will be implemented for development data

# CI/CD Simulation
ci: ## Simulate CI pipeline locally
	@echo "🔄 Running CI pipeline simulation..."
	make lint
	make test
	make docker-up
	# Add integration tests here
	make docker-down
	@echo "✅ CI pipeline completed successfully!"

# Performance
benchmark: ## Run performance benchmarks
	cd core-template && python -m pytest tests/performance/ -v

# Security
security-check: ## Run security checks
	cd core-template && bandit -r src/
	cd core-template && safety check

# Project Statistics
stats: ## Show project statistics
	@echo "📊 Project Statistics"
	@echo "===================="
	@echo "Python files: $$(find . -name '*.py' | wc -l)"
	@echo "TypeScript files: $$(find . -name '*.ts' -o -name '*.tsx' | wc -l)"
	@echo "Total lines of code: $$(find . -name '*.py' -o -name '*.ts' -o -name '*.tsx' | xargs wc -l | tail -1)"
	@echo "Test files: $$(find . -name 'test_*.py' -o -name '*_test.py' | wc -l)"

# Environment
env-check: ## Check environment setup
	@echo "🔍 Environment Check"
	@echo "==================="
	@python --version
	@node --version || echo "Node.js not installed"
	@docker --version || echo "Docker not installed"
	@docker-compose --version || echo "Docker Compose not installed"
