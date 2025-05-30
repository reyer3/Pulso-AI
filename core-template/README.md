# 🏗️ Core Template - Pulso-AI

Este directorio contiene el **template base reutilizable** que se utiliza para crear nuevas instancias de cliente.

## 🎯 Propósito

El core-template implementa la **Arquitectura Hexagonal** (Clean Architecture) que permite:

- **Reutilización**: Base común para todos los clientes
- **Aislamiento**: Lógica de negocio independiente de tecnología
- **Escalabilidad**: Nuevos clientes sin cambiar el core
- **Mantenibilidad**: Un lugar central para mejoras

## 📁 Estructura

```
core-template/
├── src/
│   ├── domain/           # 💼 Lógica de negocio pura (sin dependencias)
│   ├── application/      # 🔄 Casos de uso y orquestación
│   ├── infrastructure/   # 🔌 Adaptadores e implementaciones
│   └── api/             # 🌐 FastAPI + GraphQL
├── tests/               # 🧪 Tests organizados por capa
└── requirements/        # 📦 Dependencias por entorno
```

## 🎯 Principios de Arquitectura

### 1. **Separación de Responsabilidades**
Cada capa tiene un propósito específico y bien definido.

### 2. **Inversión de Dependencias**
- El **dominio** no depende de nada
- La **aplicación** depende solo del dominio
- La **infraestructura** implementa interfaces del dominio

### 3. **Configuración sobre Código**
- Nuevos clientes = configuración YAML
- Zero cambios de código para clientes estándar

### 4. **Testabilidad**
- Tests unitarios para dominio (sin mocks)
- Tests de integración para adaptadores
- Tests end-to-end para APIs

## 🚀 Cómo Funciona

### Flujo de Datos
```
[BigQuery/PostgreSQL] → [Infrastructure] → [Application] → [Domain] → [API] → [Frontend]
```

### Ejemplo: Nuevo Cliente
```bash
# 1. Copia template base
cp -r core-template clients/nuevo-cliente

# 2. Configura adaptador específico
# clients/nuevo-cliente/config/client.yaml

# 3. Deploy automático
python scripts/deploy_client.py nuevo-cliente
```

## 🛠️ Tecnologías

### Backend
- **Python 3.11+**: Lenguaje principal
- **FastAPI**: Framework async para APIs
- **GraphQL (Strawberry)**: Query layer dinámico
- **Polars**: ETL high-performance
- **Pydantic**: Validación y serialización

### Patterns
- **Hexagonal Architecture**: Separación limpia
- **Repository Pattern**: Abstracción de datos
- **CQRS**: Separación Command/Query
- **Dependency Injection**: Flexibilidad y testing

## 📝 Convenciones

### Naming
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

### Documentation
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

1. **Feature Development**: En core-template
2. **Testing**: Tests unitarios + integración
3. **Deployment**: A cliente de testing
4. **Validation**: Con datos reales
5. **Rollout**: A todos los clientes existentes

## 🤝 Contribución

Para contribuir al core:

1. **Branch**: `feature/core-feature-name`
2. **Tests**: Cobertura > 85%
3. **Docs**: Actualizar si es necesario
4. **Migration**: Plan para clientes existentes

---

*Este template es el corazón de Pulso-AI: una base sólida para democratizar el Business Intelligence.*
