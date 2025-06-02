# 🏗️ Plantilla Base de Servicio (Core Template)

**Resumen:** Este directorio contiene la plantilla fundamental para crear nuevos servicios backend dentro del ecosistema Pulso-AI. Está diseñada en torno a los principios de la Arquitectura Hexagonal (también conocida como Puertos y Adaptadores o Arquitectura Limpia) para asegurar una clara separación de responsabilidades, mantenibilidad y testabilidad.

**Propósito Clave y Responsabilidades:**
-   **Estandarización:** Proporcionar una estructura y un patrón arquitectónico consistentes para todos los servicios backend.
-   **Reusabilidad:** Permitir el desarrollo rápido de nuevos servicios ofreciendo un esqueleto preconfigurado.
-   **Mantenibilidad:** Promover una arquitectura limpia que aísle la lógica de negocio de la infraestructura y los mecanismos de entrega.
-   **Testabilidad:** Facilitar las pruebas unitarias, de integración y de extremo a extremo (end-to-end) definiendo claramente los límites entre componentes.

## 🚀 Quick Start

### Instalación de Dependencias (Simplificado)
```bash
# Para desarrollo (recomendado)
pip install -e .[dev]

# Para producción  
pip install -e .[prod]

# Solo dependencias base
pip install -e .
```

> **Nota:** Este proyecto usa **solo pyproject.toml** para manejar dependencias. Los archivos en `requirements/` están marcados como deprecated. Ver [requirements/README.md](requirements/README.md) para la guía de migración.

### Verificar Instalación
```bash
# Verificar que no hay conflictos
pip check

# Ejecutar tests
pytest

# Verificar imports básicos
python -c "import fastapi, pydantic, strawberry; print('✅ Core dependencies OK')"
```

## 🏛️ Implementación de la Arquitectura Hexagonal

El `core-template` materializa la Arquitectura Hexagonal, que estructura la aplicación en capas distintas:

-   **Dominio (Núcleo):** Contiene la lógica de negocio pura, entidades e interfaces de casos de uso (puertos). No tiene dependencias de ninguna otra capa.
-   **Aplicación:** Orquesta los casos de uso (servicios de aplicación) implementando los puertos del dominio. Depende únicamente de la capa de Dominio.
-   **Infraestructura:** Proporciona implementaciones concretas para las interfaces definidas en la capa de Dominio (adaptadores para bases de datos, APIs externas, etc.). Depende de las capas de Dominio y Aplicación (para implementar interfaces y ser llamada por los servicios de aplicación).
-   **API (Mecanismo de Entrega):** Expone la funcionalidad de la aplicación a través de una API (ej., REST, GraphQL). Actúa como un punto de entrada y traduce las solicitudes a llamadas de servicios de aplicación.

```
Sistemas Externos (Bases de Datos, APIs de Terceros)
       ↑ ↓
[ Adaptadores de Infraestructura ] ←─────┐
       ↑ ↓                               │ (implementa)
[   Servicios de Aplicación    ] ─────→ [ Lógica de Dominio y Puertos ]
       ↑ ↓                               │ (define)
[ API (FastAPI/GraphQL) ] ←───────────────┘
       ↑ ↓
   Clientes (Frontend, Gateway)
```

## 📁 Estructura del Directorio Explicada

La plantilla está organizada de la siguiente manera:

```
core-template/
├── src/                    # Código fuente del servicio
│   ├── domain/             # 💼 Lógica de Negocio
│   │   ├── entities/       # Entidades de dominio (Cliente, Gestion, Metrica)
│   │   ├── value_objects/  # Value objects (Enums, Identificadores)
│   │   ├── ports/          # 🔌 Interfaces/Puertos (NEW: Hexagonal Architecture)
│   │   │   ├── repositories/    # Contratos para acceso a datos
│   │   │   ├── services/        # Contratos para lógica de negocio
│   │   │   └── events/          # Contratos para eventos de dominio
│   │   └── exceptions/     # Excepciones específicas del dominio
│   ├── application/        # 🔄 Casos de Uso: Servicios de aplicación que orquestan la lógica de dominio
│   ├── infrastructure/     # 🔌 Adaptadores e Implementaciones: Implementaciones concretas de puertos
│   └── api/                # 🌐 Capa de API: FastAPI, GraphQL (Strawberry), Pydantic models
├── tests/                  # 🧪 Pruebas organizadas por tipo
│   ├── unit/               # Pruebas unitarias (domain, application)
│   ├── integration/        # Pruebas de integración (infrastructure)
│   └── e2e/                # Pruebas end-to-end (API completa)
├── pyproject.toml          # 📦 Configuración moderna de Python y dependencias
├── pytest.ini             # Configuración para Pytest
├── requirements/           # ⚠️  DEPRECATED: Ver requirements/README.md para migración
└── README.md               # Esta documentación
```

## ✨ Principios Arquitectónicos Clave

1.  **Separación de Responsabilidades**: Cada capa tiene una responsabilidad distinta y bien definida.
2.  **Inversión de Dependencias**: Las dependencias fluyen hacia adentro. La capa de Dominio es independiente. Las capas de Infraestructura y API dependen de abstracciones definidas en las capas de Dominio/Aplicación.
3.  **Interfaces Explícitas (Puertos y Adaptadores)**: La comunicación entre capas ocurre a través de interfaces bien definidas (puertos) y sus implementaciones (adaptadores).
4.  **Testabilidad**: Cada capa puede ser probada independientemente. La lógica de dominio puede ser probada unitariamente sin dependencias externas.

## 🚀 Cómo Usar Esta Plantilla

1.  **Copiar**: Duplica el directorio `core-template/` para un nuevo servicio (ej., `services/nuevo-servicio/`).
2.  **Renombrar/Refactorizar**: Ajusta los nombres (ej., nombres de módulos, nombres de clases) para reflejar el contexto delimitado del nuevo servicio.
3.  **Configurar**: Define configuraciones específicas (conexiones de base de datos, claves API) típicamente mediante variables de entorno o archivos de configuración cargados por la capa de infraestructura.
4.  **Implementar**:
    *   Define entidades y lógica de dominio en `src/domain/`
    *   Define puertos (interfaces) en `src/domain/ports/` 
    *   Crea servicios de aplicación en `src/application/`
    *   Construye adaptadores para sistemas externos en `src/infrastructure/`
    *   Expón la funcionalidad a través de `src/api/`
5.  **Probar**: Escribe pruebas exhaustivas para todas las capas usando los mocks de las interfaces.

## 🛠️ Tecnologías y Patrones

-   **Framework Backend**: Python 3.11+, FastAPI (asíncrono)
-   **GraphQL**: Strawberry para Python
-   **Manejo de Datos**: Polars (para manipulación de datos de alto rendimiento), Pydantic (para validación y serialización)
-   **Patrones Arquitectónicos**: Arquitectura Hexagonal, Patrón Repositorio, Inyección de Dependencias, CQRS (opcional)
-   **Pruebas**: Pytest, `httpx` (para pruebas de API)

## 📦 Gestión de Dependencias

Este proyecto usa **pyproject.toml** como sistema único de dependencias siguiendo las mejores prácticas modernas:

### Instalación por Entorno
```bash
# Desarrollo (incluye herramientas de testing, linting, etc.)
pip install -e .[dev]

# Producción (optimizado para deployment)
pip install -e .[prod]

# Testing (solo dependencias para tests)
pip install -e .[test]

# Solo dependencias base
pip install -e .
```

### Agregar Nuevas Dependencias
```toml
# En pyproject.toml
[project]
dependencies = [
    "nueva-dependencia>=1.0.0,<2.0.0",
]

[project.optional-dependencies]
dev = [
    "nueva-herramienta-dev>=1.0.0",
]
```

### Workflow Recomendado
```bash
# Setup inicial
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -e .[dev]

# Verificar salud de dependencias
pip check

# Desarrollo diario
pytest                    # Ejecutar tests
black .                   # Formatear código
mypy src/                 # Type checking
```

## 📝 Convenciones

### Nomenclatura (Naming)
- **Clases**: PascalCase (`ClienteService`)
- **Funciones**: snake_case (`generate_dashboard`)
- **Archivos**: snake_case (`client_repository.py`)
- **Directorios**: kebab-case (`cross-filtering/`)

### Imports
```python
# Orden de imports
import standard_library
import third_party
import local_modules
```

### Documentación
```python
def process_client_data(client_id: str) -> DashboardData:
    """Procesa datos del cliente para dashboard.
    
    Args:
        client_id: Identificador único del cliente
        
    Returns:
        Datos procesados listos para visualización
        
    Raises:
        ClientNotFoundError: Si el cliente no existe
    """
```

## 🔄 Ciclo de Desarrollo

1. **Desarrollo de Características**: En core-template
2. **Pruebas**: Pruebas unitarias + integración
3. **Despliegue**: A cliente de pruebas
4. **Validación**: Con datos reales
5. **Lanzamiento (Rollout)**: A todos los clientes existentes

## 🤝 Directrices de Contribución

Para contribuir al core:

1. **Rama (Branch)**: `feature/core-feature-name`
2. **Pruebas (Tests)**: Cobertura > 85%
3. **Documentación (Docs)**: Actualizar si es necesario
4. **Migración**: Plan para clientes existentes

---

*Esta plantilla es el corazón de los servicios backend de Pulso-AI: una base sólida para construir aplicaciones escalables, mantenibles y testeables.*
