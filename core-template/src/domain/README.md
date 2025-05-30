# 💼 Domain Layer - Business Logic

Esta capa contiene la **lógica de negocio pura** del sistema. Es el corazón de Pulso-AI.

## 🎯 Principios del Domain

### 1. **Independence First**
- **Zero dependencias externas** (no imports de frameworks)
- **Pure Python** solamente
- **Business logic only** - sin I/O, sin UI, sin database

### 2. **Business-Focused**
- **Entidades** que representan conceptos del negocio real
- **Value Objects** para datos inmutables
- **Business Rules** implementadas como métodos del dominio

### 3. **Testability**
- **Unit tests** fáciles sin mocks
- **Deterministic behavior** - mismos inputs, mismos outputs
- **Fast execution** - sin I/O = tests rápidos

## 📁 Estructura

```
domain/
├── entities/                # 🏢 Entidades de negocio
│   ├── __init__.py
│   ├── cliente.py          # Cliente con sus datos básicos
│   ├── gestion.py          # Gestión de cobranza individual
│   ├── metrica.py          # Métricas calculadas
│   └── dashboard.py        # Dashboard configuration
│
├── value_objects/          # 💎 Objetos de valor inmutables
│   ├── __init__.py
│   ├── filter_state.py     # Estado de filtros aplicados
│   ├── dimension_config.py # Configuración de dimensiones
│   ├── time_period.py      # Períodos de tiempo
│   └── calculation.py      # Cálculos y fórmulas
│
├── services/               # 🔧 Servicios de dominio
│   ├── __init__.py
│   ├── homologation_service.py    # Homologación de tipificaciones
│   ├── cross_filter_service.py    # Lógica de cross-filtering
│   ├── metric_calculator.py       # Cálculos de métricas
│   └── validation_service.py      # Validaciones de negocio
│
├── repositories/           # 📊 Interfaces (solo interfaces, no implementaciones)
│   ├── __init__.py
│   ├── client_repository.py        # Interface para datos de cliente
│   ├── dashboard_repository.py     # Interface para configuración
│   └── metric_repository.py        # Interface para métricas
│
├── exceptions/             # ⚠️ Excepciones específicas del dominio
│   ├── __init__.py
│   ├── client_exceptions.py
│   ├── validation_exceptions.py
│   └── calculation_exceptions.py
│
└── __init__.py
```

## 🏢 Entidades Principales

### Cliente
```python
@dataclass
class Cliente:
    documento: str
    nombre: str
    saldo_actual: float
    dias_mora: int
    zona: str
    segmento: str
```

### Gestión
```python
@dataclass
class Gestion:
    documento: str
    fecha: datetime
    canal: str  # CALL, VOICEBOT, EMAIL, SMS
    tipificacion_homologada: str
    es_contacto: bool
    es_compromiso: bool
```

### Métrica
```python
@dataclass
class Metrica:
    nombre: str
    valor: float
    periodo: TimePeriod
    dimensiones: Dict[str, str]
    threshold_status: str  # GOOD, WARNING, POOR
```

## 💎 Value Objects Clave

### FilterState
```python
@dataclass(frozen=True)
class FilterState:
    dimension: str
    values: Tuple[str, ...]
    operator: FilterOperator
    
    def affects_dimension(self, other_dimension: str) -> bool:
        """Determina si este filtro afecta otra dimensión"""
```

### DimensionConfig
```python
@dataclass(frozen=True)
class DimensionConfig:
    name: str
    display_name: str
    type: DimensionType
    affects_dimensions: Tuple[str, ...]
    valid_values: Optional[Tuple[str, ...]]
```

## 🔧 Servicios de Dominio

### HomologationService
Servicio para normalizar tipificaciones entre clientes:
- Movistar: "Promesa de Pago" → Universal: "COMPROMISO_PAGO"
- Claro: "Compromete Pagar" → Universal: "COMPROMISO_PAGO"

### CrossFilterService
Motor de cross-filtering inteligente:
- Aplica reglas de negocio para filtros dependientes
- Calcula sugerencias based on current state
- Mantiene consistencia en el estado del dashboard

### MetricCalculator
Calcula métricas de negocio:
- PDPs por hora = PDPs totales / horas trabajadas
- Tasa contactabilidad = (contactos / gestiones) * 100
- Efectividad = (compromisos / contactos) * 100

## 📏 Convenciones de Código

### Naming
```python
# Entidades: Sustantivos en singular
class Cliente:
    pass

# Services: Verbo + Service
class HomologationService:
    pass

# Value Objects: Descriptivo + concepto
class FilterState:
    pass
```

### Error Handling
```python
# Excepciones específicas del dominio
class ClientNotFoundError(DomainException):
    def __init__(self, client_id: str):
        super().__init__(f"Cliente {client_id} no encontrado")
```

### Business Rules
```python
# Reglas como métodos del dominio
class Gestion:
    def es_gestion_efectiva(self) -> bool:
        """Una gestión es efectiva si genera contacto o compromiso"""
        return self.es_contacto or self.es_compromiso
```

## 🧪 Testing Guidelines

### Unit Tests
```python
def test_cliente_calculates_riesgo_correctly():
    # Arrange - pure domain objects
    cliente = Cliente(
        documento="12345678",
        saldo_actual=1000.0,
        dias_mora=45
    )
    
    # Act - call domain method
    riesgo = cliente.calculate_riesgo()
    
    # Assert - verify business logic
    assert riesgo == RiesgoLevel.MEDIO
```

### No External Dependencies
```python
# ❌ NO hacer esto en domain
import requests
import pandas
from sqlalchemy import *

# ✅ SÍ hacer esto
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
```

## 🎯 Real-World Examples

### Homologación Movistar → Universal
```python
# Movistar usa sus propias tipificaciones
movistar_tipificacion = "Promesa de Pago Próxima Semana"

# El domain las normaliza
service = HomologationService()
universal = service.homologate(
    tipificacion=movistar_tipificacion,
    client="movistar-peru"
)
# Result: "COMPROMISO_PAGO"
```

### Cross-Filtering Business Logic
```python
# Cuando filtro por "Zona Norte"
filter_zona = FilterState(
    dimension="zona",
    values=("NORTE",),
    operator=FilterOperator.EQUALS
)

# El domain sabe qué ejecutivos están en esa zona
service = CrossFilterService()
suggested_ejecutivos = service.get_suggested_values(
    current_filters=[filter_zona],
    target_dimension="ejecutivo"
)
# Result: ["Juan Pérez", "María García", ...]
```

## 🚀 Business Impact

Este domain layer permite:
- **Reutilización**: La misma lógica funciona para todos los clientes
- **Testabilidad**: Business rules testeadas sin complejidad
- **Mantenimiento**: Cambios de reglas en un solo lugar
- **Escalabilidad**: Nuevos clientes sin cambiar business logic

---

*El domain es independiente de la tecnología, pero completamente enfocado en el negocio real.*
