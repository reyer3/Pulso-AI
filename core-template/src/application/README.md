# 🔄 Application Layer - Use Cases & Orchestration

Esta capa contiene los **casos de uso** del sistema y orquesta las interacciones entre el dominio y la infraestructura.

## 🎯 Propósito

La capa de aplicación:
- **Orquesta** la lógica de dominio para casos específicos
- **Coordina** between domain services and repositories
- **Maneja** transacciones y consistencia
- **No contiene** business logic (eso va en domain)

## 📁 Estructura

```
application/
├── use_cases/              # 🎯 Casos de uso principales
│   ├── __init__.py
│   ├── client/
│   │   ├── __init__.py
│   │   ├── integrate_client_data.py    # Integrar datos de cliente nuevo
│   │   ├── update_client_config.py     # Actualizar configuración
│   │   └── validate_client_data.py     # Validar datos cliente
│   │
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── generate_dashboard.py       # Generar dashboard principal
│   │   ├── apply_cross_filters.py      # Aplicar cross-filtering
│   │   ├── calculate_metrics.py        # Calcular métricas
│   │   └── export_dashboard_data.py    # Exportar datos
│   │
│   └── data/
│       ├── __init__.py
│       ├── extract_client_data.py      # ETL - Extract
│       ├── transform_data.py           # ETL - Transform  
│       ├── load_datamart.py            # ETL - Load
│       └── refresh_cache.py            # Cache management
│
├── dto/                    # 📦 Data Transfer Objects
│   ├── __init__.py
│   ├── dashboard_request.py            # Request para dashboard
│   ├── dashboard_response.py           # Response de dashboard
│   ├── filter_request.py               # Request de filtros
│   └── client_integration_dto.py       # DTO para integración
│
├── interfaces/             # 🔌 Interfaces para infraestructura
│   ├── __init__.py
│   ├── repositories/                   # Repository interfaces
│   │   ├── __init__.py
│   │   ├── client_data_repository.py
│   │   ├── dashboard_repository.py
│   │   └── cache_repository.py
│   │
│   ├── external/                       # External service interfaces
│   │   ├── __init__.py
│   │   ├── notification_service.py
│   │   ├── email_service.py
│   │   └── audit_service.py
│   │
│   └── adapters/                       # Data source interfaces
│       ├── __init__.py
│       ├── bigquery_adapter.py
│       ├── postgresql_adapter.py
│       └── api_adapter.py
│
├── commands/               # 📝 Command pattern for mutations
│   ├── __init__.py
│   ├── create_client_command.py
│   ├── update_dashboard_command.py
│   └── refresh_data_command.py
│
├── queries/                # 🔍 Query pattern for reads
│   ├── __init__.py
│   ├── dashboard_query.py
│   ├── client_metrics_query.py
│   └── cross_filter_query.py
│
├── services/               # 🛠️ Application services
│   ├── __init__.py
│   ├── dashboard_service.py            # Coordina dashboard operations
│   ├── etl_service.py                  # Coordina ETL processes
│   ├── client_service.py               # Coordina client operations
│   └── notification_service.py         # Coordina notifications
│
└── __init__.py
```

## 🎯 Use Cases Principales

### IntegrateClientDataUseCase
```python
class IntegrateClientDataUseCase:
    def __init__(
        self,
        client_repository: ClientRepository,
        data_adapter: DataAdapter,
        homologation_service: HomologationService
    ):
        self._client_repo = client_repository
        self._data_adapter = data_adapter
        self._homologation_service = homologation_service
    
    async def execute(
        self, 
        request: ClientIntegrationRequest
    ) -> ClientIntegrationResponse:
        """Integra datos de un cliente nuevo o existente."""
        
        # 1. Validate client configuration
        # 2. Extract data from source
        # 3. Transform using domain rules
        # 4. Load to datamart
        # 5. Generate initial dashboard
```

### GenerateDashboardUseCase
```python
class GenerateDashboardUseCase:
    async def execute(
        self,
        request: DashboardRequest
    ) -> DashboardResponse:
        """Genera dashboard con filtros aplicados."""
        
        # 1. Validate filters
        # 2. Apply cross-filtering rules
        # 3. Calculate metrics
        # 4. Format for frontend
        # 5. Cache results
```

### ApplyCrossFiltersUseCase
```python
class ApplyCrossFiltersUseCase:
    async def execute(
        self,
        request: CrossFilterRequest
    ) -> CrossFilterResponse:
        """Aplica cross-filtering inteligente."""
        
        # 1. Analyze current filter state
        # 2. Apply domain business rules
        # 3. Calculate suggested values
        # 4. Return updated suggestions
```

## 📦 Data Transfer Objects (DTOs)

### DashboardRequest
```python
@dataclass
class DashboardRequest:
    client_id: str
    time_period: TimePeriod
    filters: List[FilterState]
    requested_metrics: List[str]
    
    def validate(self) -> None:
        """Valida que el request esté bien formado."""
```

### DashboardResponse
```python
@dataclass
class DashboardResponse:
    client_id: str
    dashboard_data: DashboardData
    applied_filters: List[FilterState]
    suggested_filters: Dict[str, List[str]]
    metadata: DashboardMetadata
    cache_info: CacheInfo
```

## 🔌 Interfaces Pattern

### Repository Interface
```python
# En application/interfaces/repositories/
class ClientDataRepository(ABC):
    @abstractmethod
    async def get_client_data(
        self, 
        client_id: str,
        time_period: TimePeriod,
        filters: List[FilterState]
    ) -> ClientData:
        """Interface que será implementada en infrastructure."""
        pass
```

### External Service Interface
```python
# En application/interfaces/external/
class NotificationService(ABC):
    @abstractmethod
    async def send_dashboard_alert(
        self,
        client_id: str,
        alert: DashboardAlert
    ) -> None:
        pass
```

## 🛠️ Application Services

### DashboardService
```python
class DashboardService:
    """Coordina todas las operaciones de dashboard."""
    
    def __init__(
        self,
        generate_dashboard_use_case: GenerateDashboardUseCase,
        cross_filter_use_case: ApplyCrossFiltersUseCase,
        cache_service: CacheService
    ):
        self._generate_dashboard = generate_dashboard_use_case
        self._cross_filter = cross_filter_use_case
        self._cache = cache_service
    
    async def get_dashboard_with_caching(
        self,
        request: DashboardRequest
    ) -> DashboardResponse:
        """Dashboard con caching inteligente."""
        
        # Check cache first
        cached = await self._cache.get_dashboard(request)
        if cached and not cached.is_expired():
            return cached
            
        # Generate new dashboard
        dashboard = await self._generate_dashboard.execute(request)
        
        # Cache for future requests
        await self._cache.store_dashboard(request, dashboard)
        
        return dashboard
```

## 📝 Command Query Separation (CQS)

### Commands (Mutations)
```python
# Commands modifican estado
@dataclass
class CreateClientCommand:
    client_id: str
    client_name: str
    database_config: DatabaseConfig
    dimensions: List[DimensionConfig]
    
class CreateClientCommandHandler:
    async def handle(self, command: CreateClientCommand) -> ClientCreated:
        # Create client with domain validation
        pass
```

### Queries (Reads)
```python
# Queries solo leen datos
@dataclass
class DashboardQuery:
    client_id: str
    filters: List[FilterState]
    
class DashboardQueryHandler:
    async def handle(self, query: DashboardQuery) -> DashboardData:
        # Read dashboard data
        pass
```

## 🔄 Transaction Management

### Unit of Work Pattern
```python
class UnitOfWork:
    """Manages transactions across multiple repositories."""
    
    async def __aenter__(self):
        self._transaction = await self._db.begin()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self._transaction.rollback()
        else:
            await self._transaction.commit()
            
    async def commit(self):
        await self._transaction.commit()
        
    async def rollback(self):
        await self._transaction.rollback()
```

### Usage in Use Cases
```python
class IntegrateClientDataUseCase:
    async def execute(self, request: ClientIntegrationRequest):
        async with self._unit_of_work as uow:
            # Multiple operations in single transaction
            client = await self._client_repo.create(request.client_data)
            await self._dashboard_repo.create_initial_config(client.id)
            await self._data_adapter.initial_load(client.id)
            
            await uow.commit()  # All or nothing
```

## 🧪 Testing Application Layer

### Use Case Testing
```python
class TestGenerateDashboardUseCase:
    @pytest.fixture
    def use_case(self):
        # Mock all dependencies
        client_repo = Mock(spec=ClientRepository)
        metric_calculator = Mock(spec=MetricCalculator)
        
        return GenerateDashboardUseCase(
            client_repo=client_repo,
            metric_calculator=metric_calculator
        )
    
    async def test_generates_dashboard_successfully(self, use_case):
        # Arrange
        request = DashboardRequest(
            client_id="test-client",
            filters=[]
        )
        
        # Act
        response = await use_case.execute(request)
        
        # Assert
        assert response.client_id == "test-client"
        assert len(response.dashboard_data.metrics) > 0
```

## 🎯 Real-World Flow

### Scenario: Usuario aplica filtro en dashboard

1. **Frontend** envía `CrossFilterRequest`
2. **Application** valida request via DTO
3. **Use Case** orquesta domain services:
   - `CrossFilterService.get_suggested_values()`
   - `MetricCalculator.recalculate_with_filters()`
4. **Repository** interfaces fetch data needed
5. **Response** formateado y enviado al frontend

### Performance Considerations
- **Caching**: Application layer manages cache strategy
- **Batching**: Multiple repository calls batched when possible
- **Async**: All I/O operations are async
- **Circuit Breaker**: For external service calls

## 📏 Convenciones

### Error Handling
```python
# Application-specific exceptions
class ApplicationException(Exception):
    pass

class DashboardGenerationError(ApplicationException):
    def __init__(self, client_id: str, reason: str):
        super().__init__(f"Dashboard generation failed for {client_id}: {reason}")
```

### Logging
```python
# Structured logging in use cases
logger.info(
    "Dashboard generated",
    extra={
        "client_id": request.client_id,
        "filter_count": len(request.filters),
        "execution_time_ms": execution_time,
        "cache_hit": cache_hit
    }
)
```

## 🚀 Benefits

Esta arquitectura de application layer proporciona:

- **Testability**: Easy to mock dependencies and test business flows
- **Reusability**: Use cases can be composed in different ways
- **Performance**: Caching and transaction management optimized
- **Maintainability**: Clear separation between orchestration and business logic
- **Scalability**: Async operations and efficient data access

---

*La capa de aplicación es el director de orquesta que coordina todo sin tomar decisiones de negocio.*
