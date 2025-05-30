# 🚀 Pulso-AI Development Makefile
# Commands para setup y desarrollo rápido

.PHONY: help setup install-deps start-services stop-services restart-services test lint format clean logs status

# Variables
PYTHON_VERSION = 3.11
NODE_VERSION = 18
BACKEND_DIR = core-template
FRONTEND_DIR = frontend

# Colores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

## 📋 Help - Lista todos los comandos disponibles
help:
	@echo "$(BLUE)🚀 Pulso-AI Development Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup Commands:$(NC)"
	@echo "  make setup          - Setup completo del entorno de desarrollo"
	@echo "  make install-deps   - Instala todas las dependencias"
	@echo ""
	@echo "$(GREEN)Service Commands:$(NC)"
	@echo "  make start-services - Inicia servicios Docker (PostgreSQL, Redis)"
	@echo "  make stop-services  - Detiene servicios Docker"
	@echo "  make restart-services - Reinicia servicios Docker"
	@echo "  make logs          - Muestra logs de servicios"
	@echo "  make status        - Estado de servicios"
	@echo ""
	@echo "$(GREEN)Development Commands:$(NC)"
	@echo "  make test          - Ejecuta todos los tests"
	@echo "  make lint          - Ejecuta linters en todo el código"
	@echo "  make format        - Formatea todo el código"
	@echo "  make clean         - Limpia archivos temporales"
	@echo ""
	@echo "$(GREEN)Admin Tools:$(NC)"
	@echo "  make admin-tools   - Inicia Adminer y Redis Commander"
	@echo "  make db-shell      - Conecta a PostgreSQL shell"
	@echo "  make redis-shell   - Conecta a Redis shell"

## 🛠️ Setup completo del entorno de desarrollo
setup: check-requirements create-directories start-services install-deps
	@echo "$(GREEN)✅ Entorno de desarrollo configurado exitosamente!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Configura tu IDE con las settings de .vscode/"
	@echo "2. Activa pre-commit hooks: pre-commit install"
	@echo "3. Ejecuta tests: make test"
	@echo "4. Consulta la documentación: docs/development.md"

## 🔍 Verifica requirements del sistema
check-requirements:
	@echo "$(BLUE)🔍 Verificando requirements...$(NC)"
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)❌ Docker no está instalado$(NC)"; exit 1; }
	@command -v docker-compose >/dev/null 2>&1 || { echo "$(RED)❌ Docker Compose no está instalado$(NC)"; exit 1; }
	@command -v python3 >/dev/null 2>&1 || { echo "$(RED)❌ Python 3 no está instalado$(NC)"; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "$(RED)❌ Node.js no está instalado$(NC)"; exit 1; }
	@echo "$(GREEN)✅ Todos los requirements están instalados$(NC)"

## 📁 Crea directorios necesarios
create-directories:
	@echo "$(BLUE)📁 Creando estructura de directorios...$(NC)"
	@mkdir -p $(BACKEND_DIR)/src/{domain,application,infrastructure,api}
	@mkdir -p $(BACKEND_DIR)/tests/{unit,integration,e2e}
	@mkdir -p $(BACKEND_DIR)/requirements
	@mkdir -p $(FRONTEND_DIR)/src/{components,hooks,graphql,utils}
	@mkdir -p docs infrastructure/postgres shared/{auth,monitoring,utils}
	@mkdir -p clients/template
	@echo "$(GREEN)✅ Directorios creados$(NC)"

## 📦 Instala todas las dependencias
install-deps: install-backend-deps install-frontend-deps
	@echo "$(GREEN)✅ Todas las dependencias instaladas$(NC)"

## 🐍 Instala dependencias del backend
install-backend-deps:
	@echo "$(BLUE)🐍 Instalando dependencias del backend...$(NC)"
	@if [ ! -d "$(BACKEND_DIR)/venv" ]; then \
		cd $(BACKEND_DIR) && python3 -m venv venv; \
	fi
	@cd $(BACKEND_DIR) && source venv/bin/activate && pip install --upgrade pip
	@if [ -f "$(BACKEND_DIR)/requirements/dev.txt" ]; then \
		cd $(BACKEND_DIR) && source venv/bin/activate && pip install -r requirements/dev.txt; \
	fi

## ⚛️ Instala dependencias del frontend
install-frontend-deps:
	@echo "$(BLUE)⚛️ Instalando dependencias del frontend...$(NC)"
	@if [ -f "$(FRONTEND_DIR)/package.json" ]; then \
		cd $(FRONTEND_DIR) && npm install; \
	fi

## 🐳 Inicia servicios Docker
start-services:
	@echo "$(BLUE)🐳 Iniciando servicios Docker...$(NC)"
	@docker-compose up -d postgres redis
	@echo "$(GREEN)✅ Servicios iniciados$(NC)"
	@make status

## 🛑 Detiene servicios Docker
stop-services:
	@echo "$(BLUE)🛑 Deteniendo servicios Docker...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

## 🔄 Reinicia servicios Docker
restart-services:
	@echo "$(BLUE)🔄 Reiniciando servicios Docker...$(NC)"
	@docker-compose restart postgres redis
	@echo "$(GREEN)✅ Servicios reiniciados$(NC)"

## 🔧 Inicia herramientas de administración
admin-tools:
	@echo "$(BLUE)🔧 Iniciando herramientas de administración...$(NC)"
	@docker-compose --profile admin up -d adminer redis-commander
	@echo "$(GREEN)✅ Admin tools disponibles:$(NC)"
	@echo "  - Adminer (PostgreSQL): http://localhost:8080"
	@echo "  - Redis Commander: http://localhost:8081"

## 📊 Estado de servicios
status:
	@echo "$(BLUE)📊 Estado de servicios:$(NC)"
	@docker-compose ps

## 📝 Muestra logs de servicios
logs:
	@docker-compose logs -f --tail=100

## 🗄️ Conecta a PostgreSQL shell
db-shell:
	@echo "$(BLUE)🗄️ Conectando a PostgreSQL...$(NC)"
	@docker-compose exec postgres psql -U pulso_ai -d pulso_ai_dev

## 🔴 Conecta a Redis shell
redis-shell:
	@echo "$(BLUE)🔴 Conectando a Redis...$(NC)"
	@docker-compose exec redis redis-cli -a dev_redis_2024

## 🧪 Ejecuta todos los tests
test: test-backend test-frontend
	@echo "$(GREEN)✅ Todos los tests completados$(NC)"

## 🐍 Tests del backend
test-backend:
	@echo "$(BLUE)🧪 Ejecutando tests del backend...$(NC)"
	@if [ -d "$(BACKEND_DIR)/venv" ]; then \
		cd $(BACKEND_DIR) && source venv/bin/activate && \
		if command -v pytest >/dev/null 2>&1; then \
			pytest tests/ -v --cov=src --cov-report=term-missing; \
		else \
			echo "$(YELLOW)⚠️ pytest no instalado, saltando tests de backend$(NC)"; \
		fi \
	else \
		echo "$(YELLOW)⚠️ Virtual environment no encontrado, saltando tests de backend$(NC)"; \
	fi

## ⚛️ Tests del frontend
test-frontend:
	@echo "$(BLUE)🧪 Ejecutando tests del frontend...$(NC)"
	@if [ -f "$(FRONTEND_DIR)/package.json" ]; then \
		cd $(FRONTEND_DIR) && npm test; \
	else \
		echo "$(YELLOW)⚠️ Frontend no configurado, saltando tests$(NC)"; \
	fi

## 🔍 Ejecuta linters
lint: lint-backend lint-frontend
	@echo "$(GREEN)✅ Linting completado$(NC)"

## 🐍 Linting del backend
lint-backend:
	@echo "$(BLUE)🔍 Ejecutando linters del backend...$(NC)"
	@if [ -d "$(BACKEND_DIR)/venv" ]; then \
		cd $(BACKEND_DIR) && source venv/bin/activate && \
		if command -v flake8 >/dev/null 2>&1; then flake8 src/ tests/; fi && \
		if command -v mypy >/dev/null 2>&1; then mypy src/; fi; \
	fi

## ⚛️ Linting del frontend
lint-frontend:
	@echo "$(BLUE)🔍 Ejecutando linters del frontend...$(NC)"
	@if [ -f "$(FRONTEND_DIR)/package.json" ]; then \
		cd $(FRONTEND_DIR) && npm run lint; \
	fi

## 🎨 Formatea código
format: format-backend format-frontend
	@echo "$(GREEN)✅ Formato aplicado$(NC)"

## 🐍 Formato del backend
format-backend:
	@echo "$(BLUE)🎨 Formateando código del backend...$(NC)"
	@if [ -d "$(BACKEND_DIR)/venv" ]; then \
		cd $(BACKEND_DIR) && source venv/bin/activate && \
		if command -v black >/dev/null 2>&1; then black src/ tests/; fi && \
		if command -v isort >/dev/null 2>&1; then isort src/ tests/; fi; \
	fi

## ⚛️ Formato del frontend
format-frontend:
	@echo "$(BLUE)🎨 Formateando código del frontend...$(NC)"
	@if [ -f "$(FRONTEND_DIR)/package.json" ]; then \
		cd $(FRONTEND_DIR) && npm run format; \
	fi

## 🧹 Limpia archivos temporales
clean:
	@echo "$(BLUE)🧹 Limpiando archivos temporales...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".pytest_cache" -delete
	@find . -type d -name "*.egg-info" -delete
	@find . -type f -name ".coverage" -delete
	@find . -type d -name "node_modules" -prune -o -type f -name "*.log" -delete
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

## 🧨 Reset completo del entorno
reset: clean stop-services
	@echo "$(YELLOW)⚠️ Eliminando volúmenes Docker...$(NC)"
	@docker-compose down -v
	@docker system prune -f
	@echo "$(GREEN)✅ Reset completado$(NC)"
