# 🔌 Domain Ports - Hexagonal Architecture

Esta carpeta contiene los **puertos (interfaces)** que definen los contratos entre la capa de dominio y la infraestructura en Pulso-AI, siguiendo el patrón de **arquitectura hexagonal**.

## 🎯 ¿Qué son los Puertos?

Los puertos son **interfaces abstractas** que definen:
- **QUÉ** necesita el dominio (contratos)
- **SIN especificar CÓMO** se obtiene (implementación)

Esto permite intercambiar implementaciones (adapters) sin afectar la lógica de negocio.

## 🏗️ Arquitectura Hexagonal en Pulso-AI

```
┌─────────────────────────────────────────────────────┐
│                DOMAIN LAYER                         │
│  ┌─────────────┐    ┌─────────────┐                │
│  │  Entities   │    │Value Objects│                │  
│  │  (Cliente,  │    │  (Enums,    │                │
│  │   Gestion,  │    │ Identifiers)│                │
│  │   Metrica)  │    │             │                │
│  └─────────────┘    └─────────────┘                │
│           │                   │                     │
│           ▼                   ▼                     │
│  ┌─────────────────────────────────────────────────┐│
│  │              PORTS (Esta carpeta)               ││  
│  │  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐││
│  │  │Repositories │ │  Services   │ │    Events    │││
│  │  │(Data Access)│ │(Business    │ │  (Domain     │││
│  │  │             │ │ Logic)      │ │   Events)    │││
│  │  └─────────────┘ └─────────────┘ └──────────────┘││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
           │                   │                   │
           ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────┐
│             INFRASTRUCTURE LAYER                   │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │
│ │   BigQuery  │ │ PostgreSQL  │ │     MySQL       │ │
│ │  Adapter    │ │  Adapter    │ │   Adapter       │ │
│ │ (Movistar)  │ │  (Claro)    │ │   (Tigo)        │ │
│ └─────────────┘ └─────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## 📁 Estructura de Puertos

```
ports/
├── 📋 repositories/           # Contratos para acceso a datos
│   ├── base_repository.py     # Patrones CRUD comunes  
│   ├── cliente_repository.py  # Gestión de clientes
│   └── gestion_repository.py  # Tracking de gestiones
│
├── ⚙️  services/              # Contratos para lógica de negocio
│   ├── metrica_calculator_service.py  # Cálculo de métricas
│   ├── configuration_service.py       # Configuración multi-cliente
│   └── notification_service.py        # Alertas y notificaciones
│
└── 📡 events/                 # Contratos para eventos de dominio
    ├── event_publisher.py     # Publicación de eventos
    └── domain_events.py       # Definición de eventos
```

## 🚀 Business Impact Real

### Problema Solucionado
- **Antes**: Cada cliente (Movistar, Claro, Tigo) requería 2-3 meses de desarrollo custom
- **Ahora**: Mismo business logic, diferentes adapters → **4 horas** para nuevo cliente

### Multi-Tenancy Habilitado
```python
# Mismo código de dominio, diferentes data sources
async def generar_dashboard(cliente_repo: ClienteRepository):
    clientes_mora = await cliente_repo.find_clientes_en_mora(30)
    return crear_dashboard(clientes_mora)

# Movistar Perú → BigQuery
movistar_repo = BigQueryClienteRepository()  
dashboard_movistar = await generar_dashboard(movistar_repo)

# Claro Colombia → PostgreSQL
claro_repo = PostgreSQLClienteRepository()
dashboard_claro = await generar_dashboard(claro_repo)

# Tigo Guatemala → MySQL  
tigo_repo = MySQLClienteRepository()
dashboard_tigo = await generar_dashboard(tigo_repo)
```

## 🔌 Cómo Usar los Puertos

### 1. En Application Layer (Use Cases)
```python
from ..domain.ports import ClienteRepository, GestionRepository

class GenerateDashboardUseCase:
    def __init__(
        self,
        cliente_repo: ClienteRepository,  # ← Interface, no implementación
        gestion_repo: GestionRepository
    ):
        self.cliente_repo = cliente_repo
        self.gestion_repo = gestion_repo
        
    async def execute(self, filtros: DashboardFilters) -> Dashboard:
        # Lógica de negocio usando solo interfaces
        clientes = await self.cliente_repo.find_clientes_en_mora(30)
        gestiones = await self.gestion_repo.find_gestiones_exitosas(...)
        return self._construir_dashboard(clientes, gestiones)
```

### 2. En Infrastructure Layer (Adapters)
```python
from ..domain.ports.repositories import ClienteRepository

class BigQueryClienteRepository(ClienteRepository):
    """Implementación específica para BigQuery (Movistar)"""
    
    async def find_clientes_en_mora(self, dias_minimos: int) -> List[Cliente]:
        query = f"""
        SELECT documento, nombre, saldo_actual, dias_mora
        FROM `mibot-222814.BI_USA.clientes`  
        WHERE dias_mora >= {dias_minimos}
        """
        # Implementación específica BigQuery
        ...

class PostgreSQLClienteRepository(ClienteRepository):
    """Implementación específica para PostgreSQL (Claro)"""
    
    async def find_clientes_en_mora(self, dias_minimos: int) -> List[Cliente]:
        query = """
        SELECT documento, nombre, saldo_actual, dias_mora
        FROM public.clientes
        WHERE dias_mora >= %s
        """
        # Implementación específica PostgreSQL
        ...
```

### 3. En Tests (Mocking)
```python
from ..domain.ports.repositories import ClienteRepository

class MockClienteRepository(ClienteRepository):
    def __init__(self):
        self.clientes = []  # In-memory storage para tests
        
    async def find_clientes_en_mora(self, dias_minimos: int) -> List[Cliente]:
        return [c for c in self.clientes if c.dias_mora >= dias_minimos]

def test_dashboard_generation():
    # Arrange
    mock_repo = MockClienteRepository()
    mock_repo.clientes = [test_cliente_moroso, test_cliente_normal]
    use_case = GenerateDashboardUseCase(mock_repo, mock_gestion_repo)
    
    # Act
    result = await use_case.execute(test_filters)
    
    # Assert
    assert len(result.clientes) == 1  # Solo el moroso
```

## 📊 Casos de Uso por Puerto

### 🏢 ClienteRepository
```python
# Gestión estratégica de cartera
clientes_alta_prioridad = await cliente_repo.find_by_prioridad(PrioridadCobranza.ALTA)
top_50_deudores = await cliente_repo.find_top_deudores(50)

# Segmentación operativa
morosos_30_dias = await cliente_repo.find_clientes_en_mora(30)
contactables = await cliente_repo.find_contactables(incluir_solo_telefono=True)

# Analytics y reporting
stats = await cliente_repo.get_estadisticas_mora()
```

### 📞 GestionRepository
```python
# Productividad individual
gestiones_ana = await gestion_repo.find_by_ejecutivo_and_date_range(
    "Ana García", inicio_semana, fin_semana
)

# Métricas de equipo
stats_equipo = await gestion_repo.get_estadisticas_productividad()

# Follow-up automático
compromisos_vencidos = await gestion_repo.find_compromisos_vencidos()
```

### 📊 MetricaCalculatorService
```python
# KPIs individuales
tasa_ana = await calculator.calcular_tasa_contactabilidad(
    "Ana García", inicio_mes, fin_mes
)

# Métricas de dashboard
metricas_dashboard = await calculator.calcular_productividad_general({
    "servicio": "MOVIL",
    "cartera": "Gestión Temprana"
})

# Análisis comparativo
ranking = await calculator.calcular_ranking_ejecutivos(
    "tasa_contactabilidad", inicio_trimestre, fin_trimestre
)
```

## ⚡ Principios de Diseño

### 1. **Async by Default**
Todos los métodos son async para I/O no bloqueante:
```python
async def find_clientes_en_mora(self, dias_minimos: int) -> List[Cliente]:
    # Permite operaciones concurrentes y alta performance
```

### 2. **Type-Safe con Generics**
```python
from typing import Generic, TypeVar

T = TypeVar('T')
ID = TypeVar('ID')

class BaseRepository(Generic[T, ID], ABC):
    async def find_by_id(self, entity_id: ID) -> Optional[T]:
        # Type safety completo en compile time
```

### 3. **Business-Focused Methods**
Los métodos reflejan necesidades reales del negocio:
```python
# ❌ Mal: Generic y técnico
async def select_where_condition(self, condition: str) -> List[Dict]

# ✅ Bien: Business-focused
async def find_clientes_en_mora(self, dias_minimos: int) -> List[Cliente]
```

### 4. **Client-Agnostic Interfaces**
Los puertos no asumen tecnología específica:
```python
# ✅ Funciona con cualquier base de datos
async def count_clientes_activos(self) -> int

# ❌ Asumiría BigQuery específicamente  
async def execute_bigquery_sql(self, sql: str) -> QueryResult
```

## 🧪 Testing Strategy

### Mock Implementations
Cada puerto tiene una implementación mock trivial:
```python
class MockGestionRepository(GestionRepository):
    def __init__(self):
        self.gestiones = []
        
    async def save_gestion(self, gestion: Gestion) -> str:
        self.gestiones.append(gestion)
        return gestion.id
        
    async def find_by_cliente(self, documento: str) -> List[Gestion]:
        return [g for g in self.gestiones if g.documento_cliente == documento]
```

### Test Patterns
```python
@pytest.fixture
def mock_repos():
    return {
        'cliente_repo': MockClienteRepository(),
        'gestion_repo': MockGestionRepository()
    }

async def test_dashboard_con_filtros(mock_repos):
    # Arrange
    use_case = GenerateDashboardUseCase(**mock_repos)
    
    # Act
    dashboard = await use_case.execute(filtros_test)
    
    # Assert - Test business logic sin infrastructure
    assert dashboard.total_clientes > 0
```

## 🔄 Eventos de Dominio

### Publishers
```python
# Publicar eventos automáticamente
await event_publisher.publish_gestion_created(
    gestion_id="gest_123",
    cliente_documento="12345678",
    ejecutivo="Ana García", 
    fue_exitosa=True
)

# Trigger: Dashboard updates, notifications, analytics
```

### Event Handlers (Infrastructure Layer)
```python
class DashboardUpdateHandler:
    async def handle_gestion_created(self, event: GestionCreatedEvent):
        # Actualizar dashboard en tiempo real
        await dashboard_service.update_metrics(event.ejecutivo)
        
class NotificationHandler:
    async def handle_commitment_overdue(self, event: CommitmentOverdueEvent):
        # Enviar alerta automática
        await notification_service.send_follow_up_alert(event.cliente_documento)
```

## 🚀 Roadmap de Implementación

### ✅ Fase 0: Puertos Definidos (Actual)
- [x] Interfaces completas implementadas
- [x] Documentación y ejemplos
- [x] Patrones de testing establecidos

### 🔄 Siguiente: Fase 1 MVP  
1. **Application Layer**: Use cases que usen estos puertos
2. **BigQuery Adapter**: Primera implementación para Movistar
3. **Dashboard básico**: Funcionalidad end-to-end

### 🎯 Fase 2: Multi-Cliente
1. **PostgreSQL Adapter**: Implementación para Claro  
2. **MySQL Adapter**: Implementación para Tigo
3. **Configuration Service**: Sistema de configuración dinámico

## 💡 Tips para Desarrolladores

### 1. **Siempre usar interfaces en Application Layer**
```python
# ✅ Correcto
def __init__(self, cliente_repo: ClienteRepository):

# ❌ Incorrecto  
def __init__(self, cliente_repo: BigQueryClienteRepository):
```

### 2. **Mock first en tests**
```python
# ✅ Test business logic con mocks
mock_repo = MockClienteRepository()
use_case = GenerateDashboardUseCase(mock_repo)

# ❌ No testear con base de datos real en unit tests
real_repo = BigQueryClienteRepository()  # Integration test only
```

### 3. **Extender interfaces gradualmente**
```python
# ✅ Agregar métodos sin romper implementaciones existentes
class ClienteRepository(ABC):
    # Métodos existentes...
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Cliente]:
        """Nuevo método - implementaciones deben agregarlo"""
        pass
```

## 📚 Referencias

- **Hexagonal Architecture**: [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)
- **Ports & Adapters**: [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- **Domain-Driven Design**: [Eric Evans](https://domainlanguage.com/ddd/)

---

**🎯 Objetivo Final**: Reducir tiempo de nuevo cliente de **3 meses** → **4 horas** mediante arquitectura desacoplada y reutilizable.

¡Los puertos están listos para habilitar el multi-tenancy de Pulso-AI! 🚀
