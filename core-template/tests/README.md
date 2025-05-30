# 🧪 Testing Structure

**Comprehensive testing strategy** para garantizar calidad y confiabilidad en todo el sistema.

## 🎯 Testing Philosophy

- **Test-Driven Development**: Tests primero, implementación después
- **Pyramid Testing**: Muchos unit tests, algunos integration, pocos E2E
- **Client Isolation**: Tests que garantizan zero cross-client data leakage
- **Performance Testing**: Validar requirements de <3s dashboard, <200ms cross-filter

## 📁 Structure

```
core-template/tests/
├── unit/                    # Unit tests (fast, isolated)
│   ├── domain/             # Domain entities and business logic
│   ├── application/        # Use cases and services
│   ├── infrastructure/     # Adapters and external integrations
│   └── api/                # API endpoints and GraphQL resolvers
├── integration/            # Integration tests (with external services)
│   ├── database/           # Database integration tests
│   ├── redis/             # Cache integration tests
│   ├── external_apis/     # Third-party API tests
│   └── client_isolation/  # Multi-tenant isolation tests
├── e2e/                   # End-to-end tests (full system)
│   ├── dashboard/         # Dashboard functionality E2E
│   ├── cross_filtering/   # Cross-filtering E2E tests
│   └── client_workflows/  # Complete client workflows
├── performance/           # Performance and load tests
│   ├── etl_benchmarks/    # Polars ETL performance tests
│   ├── api_load_tests/    # API load testing with Locust
│   └── dashboard_perf/    # Dashboard loading performance
├── security/              # Security and compliance tests
│   ├── authentication/    # Auth mechanism tests
│   ├── authorization/     # Permission system tests
│   └── data_isolation/    # Client data isolation validation
├── fixtures/              # Test data and fixtures
│   ├── sample_data/       # Sample datasets for testing
│   ├── client_configs/    # Test client configurations
│   └── mock_responses/    # Mock API responses
├── conftest.py           # Pytest configuration and fixtures
└── README.md             # This documentation
```

## 🏷️ Test Markers

### Categorización por Velocidad
```python
@pytest.mark.unit          # Fast tests (<100ms)
@pytest.mark.integration   # Medium tests (<5s)
@pytest.mark.e2e          # Slow tests (<30s)
@pytest.mark.slow         # Very slow tests (>30s)
```

### Categorización por Dependencias
```python
@pytest.mark.database      # Requires database
@pytest.mark.redis         # Requires Redis
@pytest.mark.external      # Requires external APIs
@pytest.mark.client_specific  # Client-specific functionality
```

### Categorización por Funcionalidad
```python
@pytest.mark.cross_filtering  # Cross-filtering functionality
@pytest.mark.dashboard       # Dashboard-related tests
@pytest.mark.security        # Security-related tests
@pytest.mark.performance     # Performance validation
```

## 🧪 Testing Patterns

### Domain Entity Tests
```python
# tests/unit/domain/test_cliente.py
import pytest
from src.domain.entities import Cliente

class TestCliente:
    def test_cliente_creation_with_valid_data(self):
        cliente = Cliente(
            documento="12345678",
            nombre="Juan Pérez",
            saldo_actual=1500.0,
            dias_mora=30
        )
        assert cliente.documento == "12345678"
        assert cliente.esta_en_mora() is True
    
    def test_cliente_invalid_documento_raises_error(self):
        with pytest.raises(ValueError):
            Cliente(documento="", nombre="Juan", saldo_actual=0, dias_mora=0)
```

### Use Case Tests
```python
# tests/unit/application/test_dashboard_service.py
import pytest
from unittest.mock import Mock
from src.application.dashboard_service import DashboardService

class TestDashboardService:
    def test_generate_dashboard_with_valid_filters(self):
        # Arrange
        mock_repo = Mock()
        mock_repo.get_data.return_value = sample_data
        service = DashboardService(mock_repo)
        
        # Act
        result = service.generate_dashboard("movistar-peru", [])
        
        # Assert
        assert result.client_id == "movistar-peru"
        assert len(result.metrics) > 0
        mock_repo.get_data.assert_called_once()
```

### Integration Tests
```python
# tests/integration/database/test_bigquery_adapter.py
import pytest
from src.infrastructure.adapters import BigQueryAdapter

@pytest.mark.integration
@pytest.mark.database
class TestBigQueryAdapter:
    def test_execute_query_returns_polars_dataframe(self, bigquery_adapter):
        # Arrange
        query = "SELECT * FROM test_table LIMIT 10"
        
        # Act
        result = bigquery_adapter.execute_query(query)
        
        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) <= 10
```

### Client Isolation Tests
```python
# tests/integration/client_isolation/test_data_isolation.py
import pytest

@pytest.mark.integration
@pytest.mark.security
class TestClientDataIsolation:
    def test_movistar_cannot_access_claro_data(self, app_client):
        # Arrange
        movistar_token = create_token("user1", "movistar-peru")
        
        # Act
        response = app_client.get(
            "/api/claro-colombia/dashboard",
            headers={"Authorization": f"Bearer {movistar_token}"}
        )
        
        # Assert
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]
```

### Performance Tests
```python
# tests/performance/test_dashboard_performance.py
import pytest
import time
from locust import HttpUser, task, between

@pytest.mark.performance
class TestDashboardPerformance:
    def test_dashboard_loads_under_3_seconds(self, app_client):
        # Arrange
        start_time = time.time()
        
        # Act
        response = app_client.get("/api/movistar-peru/dashboard")
        
        # Assert
        duration = time.time() - start_time
        assert duration < 3.0
        assert response.status_code == 200

class DashboardUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def load_dashboard(self):
        self.client.get("/api/movistar-peru/dashboard")
    
    @task(3)
    def apply_cross_filter(self):
        response = self.client.post("/api/movistar-peru/cross-filter", 
                                  json={"dimension": "ejecutivo", "values": ["Juan"]})
        assert response.elapsed.total_seconds() < 0.2  # <200ms requirement
```

## 🔧 Testing Utilities

### Fixtures Comunes
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

@pytest.fixture
def app_client():
    return TestClient(app)

@pytest.fixture
def sample_client_config():
    return {
        "client_id": "test-client",
        "name": "Test Client",
        "database": {"type": "postgresql", "host": "localhost"}
    }

@pytest.fixture
def mock_database_adapter():
    mock = Mock()
    mock.execute_query.return_value = pl.DataFrame({
        "documento": ["123", "456"],
        "nombre": ["Juan", "Ana"],
        "saldo": [1000, 2000]
    })
    return mock
```

### Test Data Builders
```python
# tests/fixtures/builders.py
from dataclasses import dataclass
from typing import List

@dataclass
class ClienteBuilder:
    documento: str = "12345678"
    nombre: str = "Test User"
    saldo_actual: float = 1000.0
    dias_mora: int = 0
    
    def with_mora(self, dias: int):
        self.dias_mora = dias
        return self
    
    def with_saldo(self, saldo: float):
        self.saldo_actual = saldo
        return self
    
    def build(self) -> Cliente:
        return Cliente(
            documento=self.documento,
            nombre=self.nombre,
            saldo_actual=self.saldo_actual,
            dias_mora=self.dias_mora
        )
```

## 📊 Coverage Requirements

### Minimum Coverage
- **Unit Tests**: 90% coverage
- **Integration Tests**: 70% coverage  
- **Critical Paths**: 100% coverage (authentication, data isolation)

### Coverage Exclusions
```python
# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */migrations/*
    */venv/*
    */conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 🚀 Running Tests

### Comandos Básicos
```bash
# All tests
make test

# Solo unit tests (rápido)
make test-unit

# Solo integration tests
make test-integration

# Performance tests
make benchmark

# Tests con coverage detallado
make test-cov
```

### CI/CD Integration
```bash
# Pipeline completo (simula CI)
make ci
```

## 🔐 Security Testing

### Authentication Tests
- Token validation y expiración
- Role-based access control (RBAC)
- Cross-client access prevention

### Data Validation Tests  
- Input sanitization
- SQL injection prevention
- XSS protection

### Compliance Tests
- GDPR compliance validation
- Data retention policies
- Audit log verification

---

**Quality Gates**: Todo PR debe pasar tests automatizados con >80% coverage antes de merge.
