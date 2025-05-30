# 🚀 Pulso-AI

**Plataforma de dashboards configurables multi-cliente con cross-filtering inteligente y arquitectura hexagonal**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![GraphQL](https://img.shields.io/badge/GraphQL-16.8+-purple.svg)
![React](https://img.shields.io/badge/React-18+-blue.svg)

## 📋 Tabla de Contenidos

- [¿Qué es Pulso-AI?](#-qué-es-pulso-ai)
- [Problema que Resuelve](#-problema-que-resuelve)
- [Arquitectura](#-arquitectura)
- [Características Principales](#-características-principales)
- [Stack Tecnológico](#-stack-tecnológico)
- [Quick Start](#-quick-start)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Ejemplos de Configuración](#-ejemplos-de-configuración)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)

## 🎯 ¿Qué es Pulso-AI?

Pulso-AI es una **plataforma de business intelligence** que permite crear dashboards configurables para múltiples clientes de forma **ágil y escalable**. Reduce el tiempo de implementación de nuevos clientes de **3 meses a 4 horas**.

### 🔥 Propuesta de Valor

- **⚡ Desarrollo ágil**: Nuevo cliente configurado en horas, no meses
- **🔒 Aislamiento total**: Zero posibilidad de cross-client data access
- **🎛️ Configuración dinámica**: Dimensiones, métricas y reglas sin tocar código
- **🔄 Cross-filtering inteligente**: Filtros que se actualizan automáticamente
- **🏗️ Arquitectura limpia**: Hexagonal architecture con separación clara de responsabilidades

## 🔍 Problema que Resuelve

### Antes (Desarrollo Tradicional)
```
Cliente A: 2-3 meses de desarrollo custom
Cliente B: 2-3 meses de desarrollo custom  
Cliente C: 2-3 meses de desarrollo custom
```
- ❌ Código duplicado por cliente
- ❌ Mantenimiento nightmare
- ❌ Riesgo de data leakage entre clientes
- ❌ Scaling imposible

### Ahora (Pulso-AI)
```bash
# Nuevo cliente en 1 comando
python create_client.py tigo-guatemala "Tigo Guatemala" \
  --database postgresql --country GT
  
# Resultado: Dashboard funcionando en 4 horas
```
- ✅ Template central reutilizable
- ✅ Configuración específica por cliente
- ✅ Aislamiento garantizado
- ✅ Scaling horizontal automático

## 🏗️ Arquitectura

Pulso-AI utiliza **Hexagonal Architecture** (Clean Architecture) para máxima flexibilidad y mantenibilidad.

```
┌─────────────────────────────────────────────────────────────┐
│                    PULSO-AI ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────┤
│  🎨 FRONTEND (React + GraphQL)                             │
│  ├── Cross-filtering components                            │
│  ├── Dynamic dashboard builder                             │
│  └── Multi-tenant UI                                       │
├─────────────────────────────────────────────────────────────┤
│  🌐 API GATEWAY (FastAPI + GraphQL)                        │
│  ├── Client routing                                        │
│  ├── Dynamic schema generation                             │
│  └── Rate limiting per client                              │
├─────────────────────────────────────────────────────────────┤
│  💼 DOMAIN LAYER (Pure Python)                             │
│  ├── Business entities (Cliente, Gestion, Metrica)        │
│  ├── Value objects (FilterState, DimensionConfig)          │
│  ├── Business rules (HomologationService)                  │
│  └── Cross-filtering engine                                │
├─────────────────────────────────────────────────────────────┤
│  🔄 APPLICATION LAYER (Use Cases)                          │
│  ├── IntegrateClientDataUseCase                            │
│  ├── GenerateDashboardUseCase                              │
│  └── CrossFilterUseCase                                    │
├─────────────────────────────────────────────────────────────┤
│  🔌 INFRASTRUCTURE LAYER (Adapters)                        │
│  ├── BigQuery Adapter (Movistar)                           │
│  ├── PostgreSQL Adapter (Claro)                            │
│  ├── MySQL Adapter (Tigo)                                  │
│  └── API Adapter (External sources)                        │
├─────────────────────────────────────────────────────────────┤
│  💾 DATA SOURCES                                           │
│  ├── BigQuery (Google Cloud)                               │
│  ├── PostgreSQL (AWS RDS)                                  │
│  ├── MySQL (Azure)                                         │
│  └── REST APIs                                             │
└─────────────────────────────────────────────────────────────┘
```

### 🎯 Principios de Arquitectura

1. **Separation of Concerns**: Cada capa tiene una responsabilidad específica
2. **Dependency Inversion**: El dominio no depende de infraestructura
3. **Configuration over Code**: Nuevos clientes = configuración, no código
4. **Data Isolation**: Cada cliente tiene su propia instancia y datos
5. **Performance First**: Polars para ETL, GraphQL para queries eficientes

## ✨ Características Principales

### 🎛️ **Configuración Dinámica**
```yaml
# clients/movistar-peru/config.yaml
dimensions:
  ejecutivo:
    display_name: "Ejecutivo de Cobranza"
    type: "categorical"
    affects_dimensions: ["cartera", "servicio"]
    
metrics:
  tasa_contactabilidad:
    formula: "(contactos / total_gestiones) * 100"
    thresholds: {poor: 30, warning: 50, good: 70}
```

### 🔄 **Cross-Filtering Inteligente**
- Filtrar por "Ejecutivo" → Automáticamente sugiere valores relevantes para "Cartera"
- Click en cualquier dato → Auto-filtro instantáneo
- Estado reactivo en toda la UI

### 🏢 **Multi-Tenant por Diseño**
```
📁 clients/
├── movistar-peru/     (BigQuery, 3 replicas)
├── claro-colombia/    (PostgreSQL, 2 replicas)  
├── tigo-guatemala/    (MySQL, 1 replica)
└── template/          (Base para nuevos clientes)
```

### ⚡ **Performance Optimizada**
- **Polars**: ETL de datos 10-30x más rápido que pandas
- **GraphQL**: Queries exactas, zero over-fetching
- **Caching inteligente**: Cache por cliente con invalidación automática
- **Async everything**: I/O no bloqueante en todo el stack

## 🛠️ Stack Tecnológico

### Backend
- **🐍 Python 3.11+**: Lenguaje principal
- **⚡ FastAPI**: API framework async
- **📊 Polars**: ETL de datos high-performance  
- **🔍 GraphQL**: Query layer con Strawberry
- **🎯 Pydantic**: Validation y serialización
- **🔄 Celery**: Background tasks
- **📝 SQLAlchemy**: ORM para metadata

### Frontend  
- **⚛️ React 18**: UI framework
- **📡 Apollo Client**: GraphQL client
- **🎨 Tailwind CSS**: Styling utility-first
- **📊 Recharts**: Visualizaciones
- **🏗️ Vite**: Build tool y dev server

### Infrastructure
- **🐳 Docker**: Containerización
- **☸️ Kubernetes**: Orchestration
- **🌐 Nginx**: API Gateway y load balancer
- **📈 Prometheus + Grafana**: Monitoring
- **💾 Redis**: Caching y session storage

### Databases
- **🏢 BigQuery**: Data warehouse (Google Cloud)
- **🐘 PostgreSQL**: Relational database
- **🐬 MySQL**: Alternative SQL database
- **📄 MongoDB**: Document storage (opcional)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Node.js 18+

### 1. Clone Repository
```bash
git clone https://github.com/reyer3/Pulso-AI.git
cd Pulso-AI
```

### 2. Setup Development Environment
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows
pip install -r requirements/dev.txt

# Frontend
cd ../frontend
npm install
```

### 3. Start Development Services
```bash
# Start infrastructure
docker-compose up -d postgres redis

# Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# Start frontend  
cd ../frontend
npm run dev
```

### 4. Create Your First Client
```bash
# Create Movistar Peru as example client
python scripts/create_client.py movistar-peru "Movistar Perú" \
  --database bigquery --country PE

# Configure client (edit generated config file)
# clients/movistar-peru/config/client.yaml

# Deploy client
python scripts/deploy_client.py movistar-peru --env development
```

### 5. Access Dashboard
- **Frontend**: http://localhost:3000
- **GraphQL Playground**: http://localhost:8000/graphql
- **API Docs**: http://localhost:8000/docs

## 📁 Estructura del Proyecto

```
Pulso-AI/
├── 📚 docs/                          # Documentación
│   ├── architecture.md
│   ├── client-setup.md
│   └── api-reference.md
│
├── 🏗️ core-template/                 # Template base reutilizable
│   ├── src/
│   │   ├── domain/                   # Lógica de negocio pura
│   │   ├── application/              # Casos de uso
│   │   ├── infrastructure/           # Adaptadores
│   │   └── api/                      # FastAPI + GraphQL
│   ├── tests/
│   └── requirements/
│
├── 🏢 clients/                       # Instancias por cliente
│   ├── movistar-peru/
│   │   ├── config/                   # Configuración específica
│   │   ├── src/adapters/             # Adaptadores custom
│   │   ├── docker-compose.yml        # Deploy específico
│   │   └── k8s/                      # Manifiestos Kubernetes
│   ├── claro-colombia/
│   └── template/                     # Template para nuevos clientes
│
├── 🌐 gateway/                       # API Gateway central
│   ├── nginx.conf                    # Routing configuration
│   └── docker-compose.yml
│
├── ⚛️ frontend/                      # React application
│   ├── src/
│   │   ├── components/               # UI components
│   │   ├── hooks/                    # Custom hooks
│   │   ├── graphql/                  # GraphQL queries
│   │   └── utils/
│   └── package.json
│
├── 📜 scripts/                       # Automation scripts
│   ├── create_client.py              # Client creation
│   ├── deploy_client.py              # Deployment
│   └── backup_client.py              # Data backup
│
├── 🏗️ infrastructure/                # Infrastructure as Code
│   ├── terraform/                    # Terraform configs
│   ├── kubernetes/                   # K8s manifests
│   └── monitoring/                   # Observability
│
├── 🔧 shared/                        # Shared libraries
│   ├── auth/                         # Authentication
│   ├── monitoring/                   # Metrics & logging
│   └── utils/                        # Common utilities
│
├── 📋 ROADMAP.md                     # Development roadmap
├── 🐳 docker-compose.yml             # Development environment
└── 📝 README.md                      # This file
```

## 📊 Ejemplos de Configuración

### Cliente: Movistar Perú
```yaml
client:
  id: "movistar-peru"
  name: "Movistar Perú"
  
dimensions:
  ejecutivo:
    display_name: "Ejecutivo de Cobranza"
    type: "categorical"
    affects_dimensions: ["cartera", "servicio"]
    
  cartera:
    display_name: "Cartera de Gestión"
    valid_values: ["Gestión Temprana", "Altas Nuevas"]
    
metrics:
  pdps_por_hora:
    display_name: "PDPs por Hora"
    formula: "pdp_count / horas_trabajadas"
    thresholds: {warning: 2, good: 5}
    
database:
  type: "bigquery"
  project_id: "mibot-222814"
  dataset: "BI_USA"
```

### Cliente: Claro Colombia
```yaml
client:
  id: "claro-colombia"
  name: "Claro Colombia"
  
dimensions:
  agente:              # Diferente naming
    display_name: "Agente de Cobranza" 
    type: "categorical"
    
  linea_negocio:       # Campo específico de Claro
    display_name: "Línea de Negocio"
    valid_values: ["MOVIL", "HOGAR", "EMPRESAS"]
    
database:
  type: "postgresql"   # Diferente base de datos
  host: "claro-db.amazonaws.com"
```

## 🗺️ Roadmap

Ver [ROADMAP.md](ROADMAP.md) para el plan detallado de desarrollo.

### 🎯 Versión 1.0 (MVP)
- [x] Arquitectura hexagonal base
- [x] Sistema de configuración por cliente
- [ ] Cross-filtering básico
- [ ] Adaptadores BigQuery y PostgreSQL
- [ ] Frontend React con GraphQL
- [ ] Deploy automatizado

### 🚀 Versión 1.1 (Enhanced)
- [ ] Machine Learning para homologación automática
- [ ] Alertas en tiempo real
- [ ] Export personalizado (Excel, PDF)
- [ ] Dashboard builder drag & drop

### 🌟 Versión 2.0 (Advanced)
- [ ] Natural language queries
- [ ] Anomaly detection automático
- [ ] Embedded dashboards
- [ ] Mobile app

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor revisa nuestras [Contributing Guidelines](CONTRIBUTING.md).

### 🔄 Flujo de Desarrollo
1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### 🐛 Reportar Issues
- Usa los issue templates
- Incluye información de entorno
- Provee pasos para reproducir

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 👥 Team

- **Lead Architect**: [@reyer3](https://github.com/reyer3)

## 🙏 Acknowledgments

- Inspirado en la necesidad de democratizar el business intelligence
- Gracias a la comunidad open source por las herramientas increíbles
- Especial reconocimiento al equipo que enfrentó el problema original

---

<div align="center">
  <strong>🚀 Pulso-AI - Democratizando el Business Intelligence</strong><br>
  <em>De 3 meses a 4 horas para nuevos clientes</em>
</div>
