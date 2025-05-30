# 🛠️ Guía de Desarrollo - Pulso-AI

Esta guía te ayudará a configurar tu entorno de desarrollo local para contribuir a Pulso-AI.

## 📋 Tabla de Contenidos

- [Prerequisites](#-prerequisites)
- [Setup Rápido](#-setup-rápido)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Development Workflow](#-development-workflow)
- [Testing](#-testing)
- [Code Quality](#-code-quality)
- [Debugging](#-debugging)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🔧 Prerequisites

### Requisitos de Sistema

**Obligatorios:**
- **Docker**: 20.10+ y Docker Compose v2
- **Python**: 3.11+ (recomendado 3.11.6)
- **Node.js**: 18+ (recomendado 18.18.0)
- **Git**: 2.25+

**Opcionales pero recomendados:**
- **VS Code**: Con extensiones recomendadas
- **pyenv**: Para manejo de versiones Python
- **nvm**: Para manejo de versiones Node.js

### Verificar Prerequisites

```bash
# Verificar versiones
docker --version                # Docker version 20.10+
docker-compose --version        # Docker Compose version v2+
python --version                # Python 3.11+
node --version                  # v18+
git --version                   # git version 2.25+

# Verificar que Docker funciona
docker run hello-world
```

## 🚀 Setup Rápido

### 1. Clonar Repositorio

```bash
git clone https://github.com/reyer3/Pulso-AI.git
cd Pulso-AI
```

### 2. Setup Automático

```bash
# Un comando para configurar todo
make setup
```

Este comando ejecuta automáticamente:
- ✅ Verificación de prerequisites
- ✅ Creación de directorios necesarios
- ✅ Inicio de servicios Docker (PostgreSQL, Redis)
- ✅ Instalación de dependencias Python y Node.js
- ✅ Configuración de pre-commit hooks

### 3. Verificar Setup

```bash
# Verificar servicios
make status

# Ejecutar tests
make test

# Verificar linting
make lint
```

### 4. Acceder a la Aplicación

Una vez completado el setup:

- **Frontend Development**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **GraphQL Playground**: http://localhost:8000/graphql
- **API Docs (Swagger)**: http://localhost:8000/docs

**Admin Tools** (opcional):
```bash
make admin-tools
```
- **Adminer (PostgreSQL)**: http://localhost:8080
- **Redis Commander**: http://localhost:8081

## 📁 Estructura del Proyecto

```
Pulso-AI/
├── 🏗️ core-template/              # Backend - Template base
│   ├── src/
│   │   ├── domain/                # Lógica de negocio pura
│   │   ├── application/           # Casos de uso
│   │   ├── infrastructure/        # Adaptadores (DB, APIs)
│   │   └── api/                   # FastAPI + GraphQL
│   ├── tests/                     # Tests del backend
│   └── requirements/              # Dependencias Python
│
├── ⚛️ frontend/                    # Frontend React + TypeScript
│   ├── src/
│   │   ├── components/            # Componentes React
│   │   ├── hooks/                 # Custom hooks
│   │   ├── graphql/               # Queries y mutations
│   │   └── utils/                 # Utilidades
│   └── package.json
│
├── 🏢 clients/                     # Configuraciones por cliente
│   ├── movistar-peru/
│   ├── claro-colombia/
│   └── template/                  # Template para nuevos clientes
│
├── 🌐 gateway/                     # API Gateway (NGINX)
├── 📊 infrastructure/              # Infrastructure as Code
├── 🔧 shared/                      # Librerías compartidas
├── 📜 scripts/                     # Scripts de automatización
├── 📚 docs/                        # Documentación
├── 🐳 docker-compose.yml           # Servicios de desarrollo
├── 📝 Makefile                     # Comandos automatizados
└── 🔧 .env.example                 # Variables de entorno template
```

## 🔄 Development Workflow

### Crear una Nueva Feature

```bash
# 1. Crear branch desde main
git checkout main
git pull origin main
git checkout -b feature/nombre-descriptivo

# 2. Realizar cambios
# ... hacer cambios en el código ...

# 3. Verificar calidad
make lint          # Linting
make test          # Tests
make format        # Formateo automático

# 4. Commit con conventional commits
git add .
git commit -m "feat: descripción de la feature"

# 5. Push y crear PR
git push origin feature/nombre-descriptivo
```

### Comandos de Desarrollo Comunes

```bash
# Servicios Docker
make start-services     # Iniciar PostgreSQL y Redis
make stop-services      # Detener servicios
make restart-services   # Reiniciar servicios
make logs              # Ver logs de servicios

# Development servers
cd core-template && source venv/bin/activate && uvicorn app.main:app --reload
cd frontend && npm run dev

# Base de datos
make db-shell          # Conectar a PostgreSQL
make redis-shell       # Conectar a Redis

# Limpieza
make clean             # Limpiar archivos temporales
make reset             # Reset completo (elimina volúmenes Docker)
```

### Variables de Entorno

```bash
# Copiar template y personalizar
cp .env.example .env

# Variables importantes para desarrollo
DATABASE_URL=postgresql://pulso_ai:dev_password_2024@localhost:5432/pulso_ai_dev
REDIS_URL=redis://:dev_redis_2024@localhost:6379/0
ENVIRONMENT=development
DEBUG=True
```

## 🧪 Testing

### Backend Tests

```bash
cd core-template

# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=src --cov-report=html

# Tests específicos
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Tests por marker
pytest -m "unit"
pytest -m "integration"
pytest -m "database"
```

### Frontend Tests

```bash
cd frontend

# Ejecutar tests
npm test

# Tests con coverage
npm run test:coverage

# Tests en modo watch
npm run test:watch

# Tests UI (interfaz visual)
npm run test:ui
```

### Tests de Integración

```bash
# Test completo del sistema
make test

# Test específico de Docker environment
docker-compose up -d
# ... realizar tests manuales ...
docker-compose down
```

## 🎨 Code Quality

### Pre-commit Hooks

```bash
# Instalar hooks (automático con make setup)
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files

# Actualizar hooks
pre-commit autoupdate
```

### Linting y Formateo

```bash
# Backend (Python)
cd core-template
black src/ tests/           # Formateo
isort src/ tests/           # Organizar imports
flake8 src/ tests/          # Linting
mypy src/                   # Type checking
bandit -r src/              # Security scanning

# Frontend (TypeScript)
cd frontend
npm run format              # Prettier
npm run lint                # ESLint
npm run type-check          # TypeScript checking
```

### Configuración de IDE

#### VS Code (Recomendado)

Instalar extensiones recomendadas:
```bash
# Python
ms-python.python
ms-python.black-formatter
ms-python.isort
ms-python.mypy-type-checker

# TypeScript/React
bradlc.vscode-tailwindcss
esbenp.prettier-vscode
ms-vscode.vscode-typescript-next

# Docker
ms-azuretools.vscode-docker

# General
ms-vscode.vscode-json
redhat.vscode-yaml
eamodio.gitlens
```

Settings recomendadas (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "./core-template/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "typescript.preferences.importModuleSpecifier": "relative",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

## 🐛 Debugging

### Backend Debugging

```bash
# Logs de aplicación
tail -f logs/pulso-ai.log

# Debug con IPython
cd core-template
python -c "import ipdb; ipdb.set_trace(); import src.domain.entities"

# Debug de queries SQL
# Agregar en settings: LOG_LEVEL=DEBUG
```

### Frontend Debugging

```bash
# React Developer Tools (browser extension requerido)
# Redux DevTools (si usamos Redux)

# Logs detallados
VITE_LOG_LEVEL=verbose npm run dev

# Debug de red (Apollo Client)
# Abrir GraphQL Playground: http://localhost:8000/graphql
```

### Database Debugging

```bash
# Conectar a PostgreSQL
make db-shell

# Queries útiles
\dt                              # Listar tablas
\d table_name                    # Describir tabla
SELECT * FROM core.settings;     # Ver configuración
SELECT * FROM audit.activity_log ORDER BY created_at DESC LIMIT 10;

# Conectar a Redis
make redis-shell

# Comandos útiles
KEYS *                          # Ver todas las keys
GET key_name                    # Ver valor
MONITOR                         # Ver comandos en tiempo real
```

## 🔧 Troubleshooting

### Problemas Comunes

#### Error: "Port 5432 already in use"
```bash
# Verificar qué proceso usa el puerto
sudo lsof -i :5432

# Detener PostgreSQL local si está corriendo
sudo systemctl stop postgresql
# o en macOS
brew services stop postgresql
```

#### Error: "Docker permission denied"
```bash
# Agregar usuario al grupo docker (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Reiniciar Docker daemon
sudo systemctl restart docker
```

#### Error: "Python module not found"
```bash
# Verificar virtual environment
cd core-template
which python
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements/dev.txt
```

#### Error: "npm install fails"
```bash
# Limpiar cache npm
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### Error: "Pre-commit hooks fail"
```bash
# Actualizar hooks
pre-commit clean
pre-commit install
pre-commit run --all-files
```

### Performance Issues

#### Lento startup de Docker
```bash
# Limpiar imágenes no utilizadas
docker system prune -f

# Verificar recursos asignados a Docker
docker system df
```

#### Tests lentos
```bash
# Ejecutar tests en paralelo
cd core-template
pytest -n auto

cd frontend
npm run test -- --parallel
```

### Logs y Monitoring

```bash
# Ver logs de todos los servicios
make logs

# Logs específicos
docker-compose logs postgres
docker-compose logs redis

# Logs de aplicación
tail -f logs/pulso-ai.log

# Monitoring de recursos
docker stats
```

## 🤝 Contributing

### Workflow de Contribución

1. **Fork y clone** el repositorio
2. **Crear branch** para tu feature
3. **Realizar cambios** siguiendo las convenciones
4. **Ejecutar tests** y linting
5. **Crear Pull Request** con descripción clara

### Convenciones de Código

#### Commits (Conventional Commits)
```bash
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
style: cambios de formato (no afectan lógica)
refactor: refactoring de código
test: agregar o modificar tests
chore: tareas de mantenimiento
```

#### Python (PEP 8 + Black)
- Máximo 88 caracteres por línea
- Type hints obligatorios
- Docstrings para funciones públicas
- Snake_case para variables y funciones
- PascalCase para clases

#### TypeScript/React
- Functional components con hooks
- TypeScript strict mode
- Custom hooks para lógica reutilizable
- Props interfaces explícitas

### Code Review Checklist

- [ ] ✅ Tests pasan
- [ ] ✅ Code coverage mantiene >80%
- [ ] ✅ Linting sin errores
- [ ] ✅ Documentación actualizada
- [ ] ✅ No hay TODO/FIXME pendientes
- [ ] ✅ Performance no se degrada
- [ ] ✅ Security considerations revisadas

## 📚 Recursos Adicionales

### Documentación
- [Arquitectura del Sistema](./architecture.md)
- [API Reference](./api-reference.md)
- [Deployment Guide](./deployment.md)
- [Client Onboarding](./client-setup.md)

### Enlaces Externos
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [React Documentation](https://react.dev/)
- [Polars Documentation](https://pola.rs/)
- [TailwindCSS](https://tailwindcss.com/)

### Comunidad
- [GitHub Issues](https://github.com/reyer3/Pulso-AI/issues)
- [GitHub Discussions](https://github.com/reyer3/Pulso-AI/discussions)

---

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas configurando el entorno:

1. **Revisa esta documentación** completa
2. **Busca en [Issues](https://github.com/reyer3/Pulso-AI/issues)** existentes
3. **Crea un nuevo issue** con:
   - Comando ejecutado
   - Error completo
   - Sistema operativo
   - Versiones de Docker, Python, Node.js

¡Estamos aquí para ayudarte a contribuir exitosamente! 🚀
