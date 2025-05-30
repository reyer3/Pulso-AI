# 🔧 Shared Libraries

**Librerías compartidas** entre clientes y componentes para reutilización y consistencia.

## 🎯 Principio DRY

Evitar duplicación de código manteniendo librerías comunes que pueden ser utilizadas por:
- **Core Template**: Funcionalidad base
- **Client Instances**: Adaptadores específicos  
- **Scripts**: Utilidades de automatización
- **Infrastructure**: Módulos reutilizables

## 📁 Estructura

```
shared/
├── auth/
│   ├── jwt_handler.py       # Manejo de JWT tokens
│   ├── permissions.py       # Sistema de permisos RBAC
│   ├── oauth_client.py      # Integración OAuth2/SAML
│   └── session_manager.py   # Gestión de sesiones
├── monitoring/
│   ├── metrics.py           # Collector de métricas
│   ├── logging.py           # Configuración de logs
│   ├── health_checks.py     # Health checks estándar
│   └── alerts.py            # Sistema de alertas
├── utils/
│   ├── database.py          # Utilidades de base de datos
│   ├── cache.py             # Wrapper para Redis
│   ├── encryption.py        # Funciones de encriptación
│   ├── validation.py        # Validadores comunes
│   └── formatting.py        # Formateo de datos
├── config/
│   ├── base_settings.py     # Configuraciones base
│   ├── environment.py       # Manejo de env variables
│   ├── secrets_manager.py   # Gestión de secretos
│   └── client_loader.py     # Carga configuración cliente
├── exceptions/
│   ├── base_exceptions.py   # Excepciones base
│   ├── client_exceptions.py # Excepciones por cliente
│   └── api_exceptions.py    # Excepciones API
├── types/
│   ├── common_types.py      # Tipos TypeScript/Python comunes
│   ├── client_types.py      # Tipos específicos de cliente
│   └── api_types.py         # Tipos de API
└── README.md                # Esta documentación
```

## 🔐 Authentication & Authorization

### JWT Handler
```python
# shared/auth/jwt_handler.py
from typing import Dict, Optional
import jwt
from datetime import datetime, timedelta

class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def create_token(self, user_id: str, client_id: str, 
                    expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
            
        payload = {
            "user_id": user_id,
            "client_id": client_id,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
```

### RBAC Permissions
```python
# shared/auth/permissions.py
from enum import Enum
from typing import List, Set

class Permission(Enum):
    READ_DASHBOARD = "dashboard:read"
    WRITE_DASHBOARD = "dashboard:write"
    ADMIN_CLIENT = "client:admin"
    VIEW_ANALYTICS = "analytics:view"

class Role:
    def __init__(self, name: str, permissions: Set[Permission]):
        self.name = name
        self.permissions = permissions

# Roles predefinidos
ROLES = {
    "viewer": Role("viewer", {Permission.READ_DASHBOARD}),
    "analyst": Role("analyst", {
        Permission.READ_DASHBOARD, 
        Permission.VIEW_ANALYTICS
    }),
    "admin": Role("admin", {
        Permission.READ_DASHBOARD,
        Permission.WRITE_DASHBOARD,
        Permission.VIEW_ANALYTICS,
        Permission.ADMIN_CLIENT
    })
}
```

## 📊 Monitoring & Observability

### Metrics Collector
```python
# shared/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Métricas globales
REQUEST_COUNT = Counter('pulso_requests_total', 
                       'Total requests', ['client_id', 'endpoint'])
REQUEST_DURATION = Histogram('pulso_request_duration_seconds',
                           'Request duration', ['client_id', 'endpoint'])
ACTIVE_USERS = Gauge('pulso_active_users',
                    'Active users', ['client_id'])

def track_performance(client_id: str, endpoint: str):
    """Decorator para trackear performance"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            REQUEST_COUNT.labels(client_id=client_id, endpoint=endpoint).inc()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                REQUEST_DURATION.labels(
                    client_id=client_id, endpoint=endpoint
                ).observe(duration)
        return wrapper
    return decorator
```

### Structured Logging
```python
# shared/monitoring/logging.py
import structlog
import logging
from typing import Any, Dict

def configure_logging(client_id: str, environment: str):
    """Configura logging estructurado"""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    logger = structlog.get_logger()
    logger = logger.bind(client_id=client_id, environment=environment)
    return logger
```

## 💾 Database & Cache Utilities

### Database Helper
```python
# shared/utils/database.py
from typing import Any, Dict, List, Optional
import polars as pl
from abc import ABC, abstractmethod

class DatabaseAdapter(ABC):
    """Base adapter para diferentes databases"""
    
    @abstractmethod
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> pl.DataFrame:
        pass
    
    @abstractmethod
    def get_table_schema(self, table_name: str) -> Dict[str, str]:
        pass

class BigQueryAdapter(DatabaseAdapter):
    def __init__(self, project_id: str, credentials_path: str):
        self.project_id = project_id
        self.credentials_path = credentials_path
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> pl.DataFrame:
        # Implementación BigQuery con Polars
        pass

class PostgreSQLAdapter(DatabaseAdapter):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> pl.DataFrame:
        # Implementación PostgreSQL con Polars
        pass
```

### Cache Manager
```python
# shared/utils/cache.py
import redis
import json
from typing import Any, Optional
from datetime import timedelta

class CacheManager:
    def __init__(self, redis_url: str, default_ttl: int = 3600):
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached value"""
        ttl = ttl or self.default_ttl
        self.redis_client.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str) -> None:
        """Delete cached value"""
        self.redis_client.delete(key)
    
    def get_client_key(self, client_id: str, key: str) -> str:
        """Generate client-specific cache key"""
        return f"client:{client_id}:{key}"
```

## ⚙️ Configuration Management

### Client Configuration Loader
```python
# shared/config/client_loader.py
import yaml
from typing import Dict, Any
from pathlib import Path

class ClientConfigLoader:
    def __init__(self, clients_dir: Path):
        self.clients_dir = clients_dir
    
    def load_client_config(self, client_id: str) -> Dict[str, Any]:
        """Load complete client configuration"""
        client_dir = self.clients_dir / client_id
        
        config = {}
        config.update(self._load_yaml(client_dir / "config" / "client.yaml"))
        config.update(self._load_yaml(client_dir / "config" / "dimensions.yaml"))
        config.update(self._load_yaml(client_dir / "config" / "database.yaml"))
        
        return config
    
    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        if file_path.exists():
            with open(file_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}
```

## 🎯 Common Types

### TypeScript Types
```typescript
// shared/types/common_types.ts
export interface FilterState {
  dimension: string;
  values: string[];
  operator: 'in' | 'not_in' | 'equals';
}

export interface ClientConfig {
  id: string;
  name: string;
  database: DatabaseConfig;
  dimensions: Dimension[];
  metrics: Metric[];
}

export interface Dimension {
  id: string;
  display_name: string;
  type: 'categorical' | 'temporal' | 'numerical';
  affects_dimensions?: string[];
}

export interface Metric {
  id: string;
  display_name: string;
  formula: string;
  thresholds?: {
    warning?: number;
    good?: number;
  };
}
```

### Python Types
```python
# shared/types/common_types.py
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

@dataclass
class FilterState:
    dimension: str
    values: List[str]
    operator: str = "in"

@dataclass
class ClientConfig:
    id: str
    name: str
    database: Dict[str, Any]
    dimensions: List[Dict[str, Any]]
    metrics: List[Dict[str, Any]]

class DimensionType(Enum):
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal" 
    NUMERICAL = "numerical"
```

## 🔧 Usage Examples

### Using in Core Template
```python
# core-template/src/application/dashboard_service.py
from shared.monitoring.metrics import track_performance
from shared.utils.cache import CacheManager
from shared.config.client_loader import ClientConfigLoader

class DashboardService:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.cache = CacheManager()
        self.config_loader = ClientConfigLoader()
    
    @track_performance(client_id="movistar-peru", endpoint="generate_dashboard")
    def generate_dashboard(self, filters: List[FilterState]):
        # Implementation using shared utilities
        pass
```

### Using in Scripts
```python
# scripts/client-management/create_client.py
from shared.config.client_loader import ClientConfigLoader
from shared.utils.validation import validate_client_config

def create_client(client_id: str, template_dir: Path):
    # Use shared validation
    if not validate_client_config(config):
        raise ValueError("Invalid client configuration")
    
    # Use shared config loader
    loader = ClientConfigLoader(template_dir)
    # ... rest of implementation
```

---

**Beneficios**:
- ✅ **DRY**: Zero duplicación de código
- ✅ **Consistency**: Comportamiento uniforme entre clientes
- ✅ **Maintainability**: Cambios centralizados
- ✅ **Testing**: Librerías bien testadas
- ✅ **Performance**: Optimizaciones compartidas
