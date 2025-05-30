# 🔌 Infrastructure Layer - Adapters & External Concerns

Esta capa contiene todas las **implementaciones concretas** de interfaces definidas en el dominio y aplicación.

## 🎯 Propósito

La capa de infraestructura:
- **Implementa** las interfaces definidas en application/domain
- **Conecta** con sistemas externos (databases, APIs, services)
- **Maneja** detalles técnicos (serialización, protocolos, frameworks)
- **Adapta** datos externos al formato del dominio

## 📁 Estructura

```
infrastructure/
├── adapters/               # 🔌 Adaptadores para fuentes de datos
│   ├── __init__.py
│   ├── bigquery/
│   │   ├── __init__.py
│   │   ├── bigquery_adapter.py         # Implementación BigQuery
│   │   ├── bigquery_client.py          # Cliente BigQuery
│   │   ├── query_builder.py            # Constructor de queries
│   │   └── schema_mapper.py            # Mapeo de schemas
│   │
│   ├── postgresql/
│   │   ├── __init__.py
│   │   ├── postgresql_adapter.py       # Implementación PostgreSQL
│   │   ├── connection_pool.py          # Pool de conexiones
│   │   └── migrations/                 # Scripts de migración
│   │
│   ├── mysql/
│   │   ├── __init__.py
│   │   ├── mysql_adapter.py            # Implementación MySQL
│   │   └── connection_manager.py
│   │
│   └── api/
│       ├── __init__.py
│       ├── rest_adapter.py             # REST API calls
│       ├── soap_adapter.py             # SOAP legacy systems
│       └── webhook_adapter.py          # Webhook handling
│
├── repositories/           # 📊 Implementaciones de repositories
│   ├── __init__.py
│   ├── polars_client_repository.py     # Client repo usando Polars
│   ├── polars_dashboard_repository.py  # Dashboard repo usando Polars
│   ├── redis_cache_repository.py       # Cache usando Redis
│   └── file_config_repository.py       # Config desde archivos YAML
│
├── external_services/      # 🌐 Servicios externos
│   ├── __init__.py
│   ├── notification/
│   │   ├── __init__.py
│   │   ├── email_service.py            # Email notifications
│   │   ├── slack_service.py            # Slack integration
│   │   └── webhook_service.py          # Webhook notifications
│   │
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── prometheus_service.py       # Prometheus metrics
│   │   ├── logging_service.py          # Structured logging
│   │   └── tracing_service.py          # Distributed tracing
│   │
│   └── storage/
│       ├── __init__.py
│       ├── s3_service.py               # AWS S3 storage
│       ├── gcs_service.py              # Google Cloud Storage
│       └── local_file_service.py       # Local file system
│
├── etl/                    # 🔄 ETL implementations con Polars
│   ├── __init__.py
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── bigquery_extractor.py       # Extract from BigQuery
│   │   ├── postgresql_extractor.py     # Extract from PostgreSQL
│   │   ├── api_extractor.py            # Extract from APIs
│   │   └── file_extractor.py           # Extract from files
│   │
│   ├── transformers/
│   │   ├── __init__.py
│   │   ├── polars_transformer.py       # Core Polars transformations
│   │   ├── homologation_transformer.py # Tipification mapping
│   │   ├── metric_transformer.py       # Metric calculations
│   │   └── validation_transformer.py   # Data validation
│   │
│   └── loaders/
│       ├── __init__.py
│       ├── datamart_loader.py          # Load to datamart
│       ├── cache_loader.py             # Load to cache
│       └── export_loader.py            # Export to files/APIs
│
├── persistence/            # 💾 Persistence layer
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection_factory.py       # Database connections
│   │   ├── session_manager.py          # Session management
│   │   └── migration_manager.py        # Schema migrations
│   │
│   ├── cache/
│   │   ├── __init__.py
│   │   ├── redis_cache.py              # Redis implementation
│   │   ├── memory_cache.py             # In-memory cache
│   │   └── cache_strategy.py           # Cache invalidation
│   │
│   └── file_system/
│       ├── __init__.py
│       ├── local_storage.py            # Local file operations
│       ├── cloud_storage.py            # Cloud storage operations
│       └── config_loader.py            # Configuration loading
│
├── config/                 # ⚙️ Configuration management
│   ├── __init__.py
│   ├── settings.py                     # Application settings
│   ├── database_config.py              # Database configurations
│   ├── cache_config.py                 # Cache configurations
│   └── logging_config.py               # Logging setup
│
├── security/               # 🔒 Security implementations
│   ├── __init__.py
│   ├── authentication/
│   │   ├── __init__.py
│   │   ├── jwt_auth.py                 # JWT authentication
│   │   ├── oauth2_auth.py              # OAuth2 providers
│   │   └── api_key_auth.py             # API key authentication
│   │
│   ├── authorization/
│   │   ├── __init__.py
│   │   ├── rbac.py                     # Role-based access control
│   │   ├── client_isolation.py         # Client data isolation
│   │   └── permission_manager.py       # Permission checking
│   │
│   └── encryption/
│       ├── __init__.py
│       ├── data_encryption.py          # Data at rest encryption
│       └── transport_encryption.py     # Data in transit encryption
│
└── __init__.py
```

## 🔌 Data Adapters

### BigQuery Adapter
```python
class BigQueryAdapter(DataAdapter):
    """Implementación concreta para BigQuery."""
    
    def __init__(self, project_id: str, credentials_path: str):
        self._client = bigquery.Client.from_service_account_json(
            credentials_path
        )
        self._project_id = project_id
    
    async def extract_client_data(
        self,
        client_config: ClientConfig,
        time_period: TimePeriod,
        filters: List[FilterState]
    ) -> polars.DataFrame:
        """Extract data from BigQuery and return as Polars DataFrame."""
        
        # 1. Build SQL query based on config
        query = self._build_query(client_config, time_period, filters)
        
        # 2. Execute query
        job = self._client.query(query)
        
        # 3. Convert to Polars for high-performance processing
        pandas_df = job.to_dataframe()
        polars_df = polars.from_pandas(pandas_df)
        
        return polars_df
    
    def _build_query(
        self,
        client_config: ClientConfig,
        time_period: TimePeriod,
        filters: List[FilterState]
    ) -> str:
        """Build optimized SQL query."""
        
        builder = BigQueryBuilder(client_config)
        
        # Add time filter
        builder.add_time_filter(time_period)
        
        # Add dimension filters
        for filter_state in filters:
            builder.add_dimension_filter(filter_state)
        
        # Optimize for Polars processing
        builder.optimize_for_polars()
        
        return builder.build()
```

### PostgreSQL Adapter
```python
class PostgreSQLAdapter(DataAdapter):
    """Implementación concreta para PostgreSQL."""
    
    def __init__(self, connection_config: PostgreSQLConfig):
        self._pool = asyncpg.create_pool(
            host=connection_config.host,
            port=connection_config.port,
            database=connection_config.database,
            user=connection_config.user,
            password=connection_config.password,
            min_size=5,
            max_size=20
        )
    
    async def extract_client_data(
        self,
        client_config: ClientConfig,
        time_period: TimePeriod,
        filters: List[FilterState]
    ) -> polars.DataFrame:
        """Extract data using connection pool."""
        
        async with self._pool.acquire() as connection:
            # Build optimized query
            query, params = self._build_parameterized_query(
                client_config, time_period, filters
            )
            
            # Execute with prepared statement
            records = await connection.fetch(query, *params)
            
            # Convert to Polars efficiently
            data = [dict(record) for record in records]
            return polars.DataFrame(data)
```

## 📊 Repository Implementations

### Polars Client Repository
```python
class PolarsClientRepository(ClientRepository):
    """High-performance repository using Polars."""
    
    def __init__(self, data_adapter: DataAdapter):
        self._data_adapter = data_adapter
        self._cache = PolarsCache()
    
    async def get_client_data(
        self,
        client_id: str,
        time_period: TimePeriod,
        filters: List[FilterState]
    ) -> ClientData:
        """Get client data with Polars optimizations."""
        
        # Check cache first
        cache_key = self._build_cache_key(client_id, time_period, filters)
        cached_data = await self._cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # Extract raw data
        raw_df = await self._data_adapter.extract_client_data(
            client_id, time_period, filters
        )
        
        # Transform using Polars (10-30x faster than pandas)
        transformed_df = (
            raw_df
            .with_columns([
                pl.col("fecha").str.strptime(pl.Date, "%Y-%m-%d"),
                pl.col("saldo").cast(pl.Float64),
                pl.when(pl.col("tipificacion").is_in(CONTACT_TYPES))
                  .then(True)
                  .otherwise(False)
                  .alias("es_contacto")
            ])
            .filter(pl.col("fecha").is_between(time_period.start, time_period.end))
            .group_by(["documento", "ejecutivo"])
            .agg([
                pl.count().alias("total_gestiones"),
                pl.sum("es_contacto").alias("contactos"),
                pl.sum("saldo").alias("saldo_total")
            ])
        )
        
        # Convert to domain objects
        client_data = self._to_domain_objects(transformed_df)
        
        # Cache results
        await self._cache.set(cache_key, client_data, ttl=300)
        
        return client_data
```

## 🔄 ETL with Polars

### Polars Transformer
```python
class PolarsTransformer:
    """High-performance transformations using Polars."""
    
    def __init__(self, homologation_service: HomologationService):
        self._homologation = homologation_service
    
    def transform_gestiones(
        self, 
        raw_df: polars.DataFrame,
        client_config: ClientConfig
    ) -> polars.DataFrame:
        """Transform gestiones data using Polars expressions."""
        
        # Get homologation mapping for this client
        tipification_mapping = self._homologation.get_mapping(
            client_config.client_id
        )
        
        return (
            raw_df
            # Data type conversions
            .with_columns([
                pl.col("fecha").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S"),
                pl.col("saldo").cast(pl.Float64),
                pl.col("dias_mora").cast(pl.Int32)
            ])
            
            # Homologation of tipificaciones
            .with_columns([
                pl.col("tipificacion").map_dict(tipification_mapping)
                  .alias("tipificacion_homologada")
            ])
            
            # Business rules
            .with_columns([
                pl.when(
                    pl.col("tipificacion_homologada").is_in(CONTACT_TYPES)
                ).then(True).otherwise(False).alias("es_contacto"),
                
                pl.when(
                    pl.col("tipificacion_homologada").is_in(COMMITMENT_TYPES)
                ).then(True).otherwise(False).alias("es_compromiso")
            ])
            
            # Performance optimizations
            .filter(pl.col("fecha").is_not_null())
            .filter(pl.col("documento").str.lengths() > 0)
            
            # Sort for optimal query performance
            .sort(["fecha", "documento"])
        )
    
    def calculate_metrics(
        self,
        gestiones_df: polars.DataFrame,
        metric_configs: List[MetricConfig]
    ) -> polars.DataFrame:
        """Calculate metrics using Polars aggregations."""
        
        metrics_expressions = []
        
        for metric_config in metric_configs:
            if metric_config.name == "pdps_por_hora":
                expr = (
                    pl.count().alias("total_pdps") / 
                    pl.col("horas_trabajadas").sum()
                ).alias("pdps_por_hora")
                metrics_expressions.append(expr)
                
            elif metric_config.name == "tasa_contactabilidad":
                expr = (
                    pl.sum("es_contacto") * 100.0 / 
                    pl.count()
                ).alias("tasa_contactabilidad")
                metrics_expressions.append(expr)
        
        return (
            gestiones_df
            .group_by(["ejecutivo", "fecha"])
            .agg(metrics_expressions)
        )
```

## 💾 Persistence Layer

### Redis Cache Implementation
```python
class RedisCacheRepository(CacheRepository):
    """Redis-based caching with serialization."""
    
    def __init__(self, redis_config: RedisConfig):
        self._redis = aioredis.from_url(
            f"redis://{redis_config.host}:{redis_config.port}",
            password=redis_config.password,
            db=redis_config.db
        )
    
    async def get_dashboard(
        self, 
        cache_key: str
    ) -> Optional[DashboardData]:
        """Get cached dashboard data."""
        
        cached_bytes = await self._redis.get(cache_key)
        if not cached_bytes:
            return None
        
        # Deserialize using msgpack (faster than JSON)
        cached_dict = msgpack.unpackb(cached_bytes)
        
        # Convert back to domain objects
        return DashboardData.from_dict(cached_dict)
    
    async def set_dashboard(
        self,
        cache_key: str,
        dashboard_data: DashboardData,
        ttl: int = 300
    ) -> None:
        """Cache dashboard data with TTL."""
        
        # Serialize domain objects
        serialized_data = msgpack.packb(dashboard_data.to_dict())
        
        # Store with expiration
        await self._redis.setex(cache_key, ttl, serialized_data)
    
    async def invalidate_client_cache(self, client_id: str) -> None:
        """Invalidate all cache entries for a client."""
        
        pattern = f"dashboard:{client_id}:*"
        keys = await self._redis.keys(pattern)
        
        if keys:
            await self._redis.delete(*keys)
```

## 🌐 External Services

### Email Notification Service
```python
class EmailNotificationService(NotificationService):
    """Email notifications using SendGrid."""
    
    def __init__(self, sendgrid_config: SendGridConfig):
        self._sg = sendgrid.SendGridAPIClient(
            api_key=sendgrid_config.api_key
        )
        self._from_email = sendgrid_config.from_email
    
    async def send_dashboard_alert(
        self,
        client_id: str,
        alert: DashboardAlert
    ) -> None:
        """Send dashboard alert via email."""
        
        # Get client contact info
        client_config = await self._get_client_config(client_id)
        
        # Build email content
        email_content = self._build_alert_email(alert, client_config)
        
        # Send email
        message = Mail(
            from_email=self._from_email,
            to_emails=client_config.alert_emails,
            subject=f"Dashboard Alert - {alert.metric_name}",
            html_content=email_content
        )
        
        try:
            response = await self._sg.send(message)
            logger.info(f"Alert sent to {client_id}", extra={
                "status_code": response.status_code,
                "alert_type": alert.alert_type
            })
        except Exception as e:
            logger.error(f"Failed to send alert to {client_id}", extra={
                "error": str(e),
                "alert_type": alert.alert_type
            })
            raise NotificationError(f"Email sending failed: {e}")
```

## ⚙️ Configuration Management

### Settings with Environment Variables
```python
# infrastructure/config/settings.py
class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database settings
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "pulso_ai"
    postgres_user: str
    postgres_password: str
    
    # BigQuery settings
    bigquery_project_id: str
    bigquery_credentials_path: str
    
    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    
    # Security settings
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Monitoring
    enable_prometheus: bool = True
    enable_tracing: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

## 🔒 Security Implementation

### Client Data Isolation
```python
class ClientIsolationMiddleware:
    """Ensures complete client data isolation."""
    
    async def __call__(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """Middleware to enforce client isolation."""
        
        # Extract client_id from JWT token
        token = self._extract_token(request)
        client_id = self._validate_and_extract_client_id(token)
        
        # Add client_id to request context
        request.state.client_id = client_id
        
        # Execute request
        response = await call_next(request)
        
        # Ensure no cross-client data leakage in response
        self._validate_response_client_isolation(response, client_id)
        
        return response
    
    def _validate_response_client_isolation(
        self,
        response: Response,
        expected_client_id: str
    ) -> None:
        """Validate that response only contains data for expected client."""
        
        # Parse response body (only in debug mode for performance)
        if settings.enable_security_validation:
            response_data = json.loads(response.body)
            
            # Check all data entries have correct client_id
            for item in response_data.get("data", []):
                if item.get("client_id") != expected_client_id:
                    raise SecurityError(
                        f"Cross-client data leak detected: "
                        f"expected {expected_client_id}, found {item.get('client_id')}"
                    )
```

## 🧪 Testing Infrastructure

### Integration Tests
```python
class TestBigQueryAdapter:
    @pytest.fixture
    async def adapter(self):
        """Real BigQuery adapter for integration tests."""
        return BigQueryAdapter(
            project_id="test-project",
            credentials_path="test-credentials.json"
        )
    
    @pytest.mark.integration
    async def test_extract_client_data_real_bigquery(self, adapter):
        """Test with real BigQuery (requires credentials)."""
        
        client_config = ClientConfig(
            client_id="test-client",
            dataset="test_dataset",
            table="test_table"
        )
        
        time_period = TimePeriod(
            start=datetime(2024, 1, 1),
            end=datetime(2024, 1, 31)
        )
        
        # Should return Polars DataFrame
        result = await adapter.extract_client_data(
            client_config, time_period, []
        )
        
        assert isinstance(result, polars.DataFrame)
        assert len(result) > 0
        assert "documento" in result.columns
```

## 📏 Performance Considerations

### Polars Optimizations
- **Lazy evaluation**: Use `.lazy()` for complex transformations
- **Column selection**: Only select needed columns
- **Predicate pushdown**: Apply filters early
- **Memory management**: Process in chunks for large datasets

### Caching Strategy
- **Multi-level**: Memory → Redis → Database
- **Smart invalidation**: Invalidate only affected cache entries
- **TTL management**: Different TTLs for different data types
- **Cache warming**: Pre-populate cache for common queries

### Database Optimizations
- **Connection pooling**: Reuse database connections
- **Prepared statements**: Avoid SQL injection and improve performance
- **Batch operations**: Group multiple operations
- **Index optimization**: Ensure proper indexes exist

## 🚀 Real-World Benefits

Esta infrastructure layer provides:

- **Performance**: Polars delivers 10-30x speedup over pandas
- **Reliability**: Connection pooling and retry mechanisms
- **Security**: Complete client data isolation
- **Scalability**: Async operations and efficient caching
- **Maintainability**: Clear adapter pattern for new data sources

---

*La infraestructura es donde la arquitectura limpia se encuentra con el mundo real.*
