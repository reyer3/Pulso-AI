# 🌐 API Layer - FastAPI + GraphQL Interface

Esta capa expone la funcionalidad del sistema a través de **FastAPI** y **GraphQL**, proporcionando interfaces modernas y eficientes.

## 🎯 Propósito

La capa de API:
- **Expone** casos de uso como endpoints HTTP/GraphQL
- **Maneja** autenticación y autorización
- **Valida** requests y responses
- **Documenta** APIs automáticamente
- **Aplica** rate limiting y middleware

## 📁 Estructura

```
api/
├── graphql/                # 🔍 GraphQL implementation
│   ├── __init__.py
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── dashboard_schema.py         # Dashboard GraphQL schema
│   │   ├── client_schema.py            # Client management schema
│   │   ├── metric_schema.py            # Metrics and KPIs schema
│   │   └── filter_schema.py            # Cross-filtering schema
│   │
│   ├── resolvers/
│   │   ├── __init__.py
│   │   ├── dashboard_resolvers.py      # Dashboard query/mutation resolvers
│   │   ├── client_resolvers.py         # Client management resolvers
│   │   ├── metric_resolvers.py         # Metric calculation resolvers
│   │   └── filter_resolvers.py         # Cross-filter resolvers
│   │
│   ├── types/
│   │   ├── __init__.py
│   │   ├── dashboard_types.py          # GraphQL types for dashboards
│   │   ├── client_types.py             # GraphQL types for clients
│   │   ├── metric_types.py             # GraphQL types for metrics
│   │   ├── filter_types.py             # GraphQL types for filters
│   │   └── scalar_types.py             # Custom scalar types
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py          # Authentication middleware
│   │   ├── rate_limit_middleware.py    # Rate limiting per client
│   │   ├── logging_middleware.py       # Request/response logging
│   │   └── error_middleware.py         # Error handling
│   │
│   └── utils/
│       ├── __init__.py
│       ├── query_complexity.py         # Query complexity analysis
│       ├── cache_hints.py              # GraphQL caching hints
│       └── schema_generator.py         # Dynamic schema generation
│
├── rest/                   # 🛠️ REST API for management
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── clients.py                  # Client management endpoints
│   │   ├── health.py                   # Health check endpoints
│   │   ├── admin.py                    # Admin operations
│   │   └── webhooks.py                 # Webhook handling
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── cors_middleware.py          # CORS handling
│   │   ├── compression_middleware.py   # Response compression
│   │   └── security_middleware.py      # Security headers
│   │
│   └── utils/
│       ├── __init__.py
│       ├── response_models.py          # Pydantic response models
│       ├── error_handlers.py           # Custom error handlers
│       └── validators.py               # Request validators
│
├── auth/                   # 🔒 Authentication & Authorization
│   ├── __init__.py
│   ├── jwt_auth.py                     # JWT token handling
│   ├── api_key_auth.py                 # API key authentication
│   ├── oauth2_auth.py                  # OAuth2 provider integration
│   ├── permissions.py                  # Permission checking
│   └── client_isolation.py             # Client data isolation
│
├── dependencies/           # 🔧 FastAPI dependency injection
│   ├── __init__.py
│   ├── auth_dependencies.py            # Authentication dependencies
│   ├── client_dependencies.py          # Client context dependencies
│   ├── rate_limit_dependencies.py      # Rate limiting dependencies
│   └── database_dependencies.py        # Database session dependencies
│
├── models/                 # 📋 API request/response models
│   ├── __init__.py
│   ├── dashboard_models.py             # Dashboard API models
│   ├── client_models.py                # Client management models
│   ├── filter_models.py                # Filter request models
│   ├── error_models.py                 # Error response models
│   └── pagination_models.py            # Pagination models
│
├── routers/                # 🗂️ FastAPI routers
│   ├── __init__.py
│   ├── graphql_router.py               # GraphQL endpoint setup
│   ├── health_router.py                # Health check routes
│   ├── admin_router.py                 # Admin panel routes
│   └── webhook_router.py               # Webhook routes
│
├── config/                 # ⚙️ API configuration
│   ├── __init__.py
│   ├── cors_config.py                  # CORS configuration
│   ├── rate_limit_config.py            # Rate limiting config
│   └── openapi_config.py               # OpenAPI/Swagger config
│
├── main.py                 # 🚀 FastAPI application entry point
└── __init__.py
```

## 🔍 GraphQL Implementation

### Dynamic Schema Generation
```python
# graphql/utils/schema_generator.py
class DynamicSchemaGenerator:
    """Generates GraphQL schema based on client configuration."""
    
    def __init__(self, schema_registry: SchemaRegistry):
        self._registry = schema_registry
    
    def generate_dashboard_schema(
        self, 
        client_config: ClientConfig
    ) -> strawberry.Schema:
        """Generate client-specific dashboard schema."""
        
        # Base dashboard type
        @strawberry.type
        class Dashboard:
            client_id: str
            last_updated: datetime
            
        # Dynamic dimension types based on client config
        dimension_types = {}
        for dimension in client_config.dimensions:
            dimension_types[dimension.name] = self._create_dimension_type(
                dimension
            )
        
        # Dynamic metric types based on client config
        metric_types = {}
        for metric in client_config.metrics:
            metric_types[metric.name] = self._create_metric_type(metric)
        
        # Build complete schema
        schema = strawberry.Schema(
            query=self._build_query_type(dimension_types, metric_types),
            mutation=self._build_mutation_type(),
            subscription=self._build_subscription_type()
        )
        
        return schema
```

### Dashboard Query Resolver
```python
# graphql/resolvers/dashboard_resolvers.py
@strawberry.type
class DashboardQuery:
    """Main dashboard queries."""
    
    @strawberry.field
    async def dashboard(
        self,
        client_id: str,
        filters: Optional[List[FilterInput]] = None,
        time_period: Optional[TimePeriodInput] = None,
        info: strawberry.Info = strawberry.Info
    ) -> DashboardType:
        """Get dashboard data with filters."""
        
        # Get dependencies from context
        dashboard_service = info.context["dashboard_service"]
        current_user = info.context["current_user"]
        
        # Validate client access
        if not await self._can_access_client(current_user, client_id):
            raise GraphQLError("Access denied to client data")
        
        # Build request DTO
        request = DashboardRequest(
            client_id=client_id,
            filters=filters or [],
            time_period=time_period or TimePeriod.current_month(),
            user_id=current_user.id
        )
        
        # Execute use case
        response = await dashboard_service.get_dashboard_with_caching(request)
        
        # Convert to GraphQL types
        return DashboardType.from_domain(response.dashboard_data)
    
    @strawberry.field
    async def cross_filter_suggestions(
        self,
        client_id: str,
        current_filters: List[FilterInput],
        target_dimension: str,
        info: strawberry.Info
    ) -> CrossFilterSuggestionsType:
        """Get cross-filter suggestions for a dimension."""
        
        cross_filter_service = info.context["cross_filter_service"]
        current_user = info.context["current_user"]
        
        # Validate access
        if not await self._can_access_client(current_user, client_id):
            raise GraphQLError("Access denied")
        
        # Execute cross-filtering
        request = CrossFilterRequest(
            client_id=client_id,
            current_filters=current_filters,
            target_dimension=target_dimension
        )
        
        response = await cross_filter_service.get_suggestions(request)
        
        return CrossFilterSuggestionsType.from_domain(response)
```

### Client-Specific GraphQL Types
```python
# graphql/types/dashboard_types.py
def create_dynamic_dashboard_type(client_config: ClientConfig):
    """Create dashboard type specific to client configuration."""
    
    # Dynamic fields based on client dimensions
    dimension_fields = {}
    for dimension in client_config.dimensions:
        field_type = List[str] if dimension.type == "categorical" else str
        dimension_fields[f"{dimension.name}_values"] = strawberry.field(
            resolver=lambda self, dimension_name=dimension.name: 
            self.get_dimension_values(dimension_name)
        )
    
    # Dynamic metric fields
    metric_fields = {}
    for metric in client_config.metrics:
        metric_fields[metric.name] = strawberry.field(
            resolver=lambda self, metric_name=metric.name:
            self.get_metric_value(metric_name)
        )
    
    # Combine all fields
    all_fields = {
        "client_id": str,
        "last_updated": datetime,
        "total_records": int,
        **dimension_fields,
        **metric_fields
    }
    
    # Create dynamic type
    DynamicDashboardType = strawberry.type(
        type("DashboardType", (), all_fields)
    )
    
    return DynamicDashboardType
```

## 🛠️ REST API for Management

### Client Management Endpoints
```python
# rest/v1/clients.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: CreateClientRequest,
    current_user: User = Depends(get_current_admin_user),
    client_service: ClientService = Depends(get_client_service)
) -> ClientResponse:
    """Create a new client configuration."""
    
    try:
        # Execute use case
        request = CreateClientCommand(
            client_id=client_data.client_id,
            name=client_data.name,
            database_config=client_data.database_config,
            dimensions=client_data.dimensions,
            metrics=client_data.metrics,
            created_by=current_user.id
        )
        
        result = await client_service.create_client(request)
        
        return ClientResponse.from_domain(result)
        
    except ClientAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: str,
    current_user: User = Depends(get_current_user),
    client_service: ClientService = Depends(get_client_service)
) -> ClientResponse:
    """Get client configuration."""
    
    # Check permissions
    if not await can_access_client(current_user, client_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        client = await client_service.get_client(client_id)
        return ClientResponse.from_domain(client)
    except ClientNotFoundError:
        raise HTTPException(status_code=404, detail="Client not found")

@router.put("/{client_id}/config", response_model=ClientResponse)
async def update_client_config(
    client_id: str,
    config_update: UpdateClientConfigRequest,
    current_user: User = Depends(get_current_admin_user),
    client_service: ClientService = Depends(get_client_service)
) -> ClientResponse:
    """Update client configuration."""
    
    try:
        request = UpdateClientConfigCommand(
            client_id=client_id,
            dimensions=config_update.dimensions,
            metrics=config_update.metrics,
            database_config=config_update.database_config,
            updated_by=current_user.id
        )
        
        result = await client_service.update_config(request)
        
        # Invalidate GraphQL schema cache
        await invalidate_schema_cache(client_id)
        
        return ClientResponse.from_domain(result)
        
    except ClientNotFoundError:
        raise HTTPException(status_code=404, detail="Client not found")
```

### Health Check Endpoints
```python
# rest/v1/health.py
@router.get("/health", response_model=HealthResponse)
async def health_check(
    health_service: HealthService = Depends(get_health_service)
) -> HealthResponse:
    """Comprehensive health check."""
    
    checks = await health_service.run_all_checks()
    
    overall_status = "healthy" if all(
        check.status == "healthy" for check in checks
    ) else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        checks=checks,
        version=get_app_version()
    )

@router.get("/health/ready", response_model=ReadinessResponse)
async def readiness_check(
    health_service: HealthService = Depends(get_health_service)
) -> ReadinessResponse:
    """Kubernetes readiness probe."""
    
    # Check critical dependencies
    database_ready = await health_service.check_database()
    cache_ready = await health_service.check_cache()
    
    ready = database_ready and cache_ready
    
    if not ready:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    return ReadinessResponse(ready=True)
```

## 🔒 Authentication & Authorization

### JWT Authentication
```python
# auth/jwt_auth.py
class JWTAuth:
    """JWT token handling for API authentication."""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self._secret_key = secret_key
        self._algorithm = algorithm
    
    def create_access_token(
        self,
        user_id: str,
        client_id: str,
        permissions: List[str],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token with client isolation."""
        
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=30)
        )
        
        payload = {
            "sub": user_id,  # Subject (user ID)
            "client_id": client_id,  # Client isolation
            "permissions": permissions,  # User permissions
            "exp": expire,  # Expiration
            "iat": datetime.utcnow(),  # Issued at
            "type": "access_token"
        }
        
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
    
    async def verify_token(self, token: str) -> TokenPayload:
        """Verify and decode JWT token."""
        
        try:
            payload = jwt.decode(
                token, self._secret_key, algorithms=[self._algorithm]
            )
            
            # Validate required fields
            if not payload.get("sub") or not payload.get("client_id"):
                raise InvalidTokenError("Missing required token fields")
            
            # Check expiration
            if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                raise ExpiredTokenError("Token has expired")
            
            return TokenPayload(
                user_id=payload["sub"],
                client_id=payload["client_id"],
                permissions=payload.get("permissions", []),
                expires_at=datetime.fromtimestamp(payload["exp"])
            )
            
        except jwt.PyJWTError as e:
            raise InvalidTokenError(f"Token validation failed: {e}")
```

### Client Isolation Dependency
```python
# dependencies/client_dependencies.py
async def get_current_client_context(
    request: Request,
    token: str = Depends(get_jwt_token)
) -> ClientContext:
    """Get current client context with isolation validation."""
    
    # Verify token and extract client_id
    auth_service = request.app.state.auth_service
    token_payload = await auth_service.verify_token(token)
    
    # Validate client access
    client_service = request.app.state.client_service
    client = await client_service.get_client(token_payload.client_id)
    
    if not client:
        raise HTTPException(
            status_code=404, 
            detail="Client not found or access denied"
        )
    
    # Create client context
    context = ClientContext(
        client_id=client.id,
        client_name=client.name,
        user_id=token_payload.user_id,
        permissions=token_payload.permissions,
        database_config=client.database_config
    )
    
    # Store in request state for middleware access
    request.state.client_context = context
    
    return context
```

## 🚀 FastAPI Application Setup

### Main Application
```python
# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="Pulso-AI API",
        description="Multi-tenant dashboard platform API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Add compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Add security middleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(ClientIsolationMiddleware)
    app.add_middleware(RateLimitMiddleware)
    
    # Setup GraphQL
    schema = create_graphql_schema()
    graphql_app = GraphQLRouter(
        schema,
        context_getter=get_graphql_context,
        graphiql=settings.enable_graphiql
    )
    app.include_router(graphql_app, prefix="/graphql")
    
    # Setup REST endpoints
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(client_router, prefix="/api/v1")
    app.include_router(admin_router, prefix="/api/v1")
    
    # Setup application state
    setup_application_state(app)
    
    return app

async def get_graphql_context(request: Request) -> dict:
    """Create GraphQL context with dependencies."""
    
    # Get client context from middleware
    client_context = getattr(request.state, "client_context", None)
    
    # Get services from application state
    return {
        "request": request,
        "client_context": client_context,
        "dashboard_service": request.app.state.dashboard_service,
        "cross_filter_service": request.app.state.cross_filter_service,
        "client_service": request.app.state.client_service,
        "current_user": getattr(request.state, "current_user", None)
    }

def setup_application_state(app: FastAPI) -> None:
    """Initialize application services and dependencies."""
    
    # Initialize settings
    app.state.settings = get_settings()
    
    # Initialize services (with dependency injection)
    app.state.auth_service = create_auth_service()
    app.state.dashboard_service = create_dashboard_service()
    app.state.cross_filter_service = create_cross_filter_service()
    app.state.client_service = create_client_service()
    app.state.health_service = create_health_service()

# Application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
        access_log=True
    )
```

## 📊 API Models (Pydantic)

### Dashboard API Models
```python
# models/dashboard_models.py
class DashboardRequest(BaseModel):
    """Request model for dashboard data."""
    
    client_id: str = Field(..., description="Client identifier")
    time_period: Optional[TimePeriodRequest] = Field(
        default=None,
        description="Time period for data filtering"
    )
    filters: List[FilterRequest] = Field(
        default=[],
        description="Dimension filters to apply"
    )
    requested_metrics: Optional[List[str]] = Field(
        default=None,
        description="Specific metrics to calculate"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "client_id": "movistar-peru",
                "time_period": {
                    "start": "2024-01-01",
                    "end": "2024-01-31"
                },
                "filters": [
                    {
                        "dimension": "ejecutivo",
                        "values": ["Juan Pérez", "María García"],
                        "operator": "IN"
                    }
                ],
                "requested_metrics": ["pdps_por_hora", "tasa_contactabilidad"]
            }
        }

class DashboardResponse(BaseModel):
    """Response model for dashboard data."""
    
    client_id: str
    dashboard_data: DashboardData
    applied_filters: List[FilterState]
    suggested_filters: Dict[str, List[str]]
    metadata: DashboardMetadata
    cache_info: Optional[CacheInfo] = None
    
    @classmethod
    def from_domain(cls, domain_response: DashboardResponse) -> "DashboardResponse":
        """Convert from domain response to API model."""
        return cls(
            client_id=domain_response.client_id,
            dashboard_data=DashboardData.from_domain(domain_response.dashboard_data),
            applied_filters=[
                FilterState.from_domain(f) for f in domain_response.applied_filters
            ],
            suggested_filters=domain_response.suggested_filters,
            metadata=DashboardMetadata.from_domain(domain_response.metadata),
            cache_info=CacheInfo.from_domain(domain_response.cache_info) if domain_response.cache_info else None
        )
```

## 🔄 Middleware Implementation

### Rate Limiting Middleware
```python
# middleware/rate_limit_middleware.py
class RateLimitMiddleware:
    """Rate limiting per client with Redis backend."""
    
    def __init__(self, redis_client: Redis):
        self._redis = redis_client
        self._default_limit = 1000  # requests per hour
        self._client_limits = {}  # per-client overrides
    
    async def __call__(
        self, 
        request: Request, 
        call_next: Callable
    ) -> Response:
        """Apply rate limiting based on client."""
        
        # Get client context
        client_context = getattr(request.state, "client_context", None)
        
        if client_context:
            # Apply client-specific rate limiting
            limit = self._client_limits.get(
                client_context.client_id,
                self._default_limit
            )
            
            key = f"rate_limit:{client_context.client_id}:{datetime.now().hour}"
            current_count = await self._redis.incr(key)
            
            # Set expiration on first request of the hour
            if current_count == 1:
                await self._redis.expire(key, 3600)  # 1 hour
            
            if current_count > limit:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "limit": limit,
                        "reset_at": datetime.now().replace(
                            minute=0, second=0, microsecond=0
                        ) + timedelta(hours=1)
                    }
                )
        
        # Continue with request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current_count))
        
        return response
```

## 🧪 API Testing

### GraphQL Testing
```python
class TestDashboardGraphQL:
    @pytest.fixture
    async def graphql_client(self):
        """GraphQL test client with auth."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Get auth token
            token = await self._get_test_token("test-client")
            client.headers.update({"Authorization": f"Bearer {token}"})
            yield client
    
    async def test_dashboard_query(self, graphql_client):
        """Test dashboard GraphQL query."""
        
        query = """
        query GetDashboard($clientId: String!, $filters: [FilterInput!]) {
            dashboard(clientId: $clientId, filters: $filters) {
                clientId
                lastUpdated
                totalRecords
                ejecutivoValues
                pdpsPorHora
                tasaContactabilidad
            }
        }
        """
        
        variables = {
            "clientId": "test-client",
            "filters": [
                {
                    "dimension": "zona",
                    "values": ["NORTE"],
                    "operator": "IN"
                }
            ]
        }
        
        response = await graphql_client.post(
            "/graphql",
            json={"query": query, "variables": variables}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data
        assert data["data"]["dashboard"]["clientId"] == "test-client"
        assert data["data"]["dashboard"]["totalRecords"] > 0
```

## 🚀 Performance & Monitoring

### Query Complexity Analysis
```python
# graphql/utils/query_complexity.py
class QueryComplexityAnalyzer:
    """Analyze and limit GraphQL query complexity."""
    
    def __init__(self, max_complexity: int = 1000):
        self._max_complexity = max_complexity
    
    def analyze_query(self, query: str, variables: dict) -> int:
        """Calculate query complexity score."""
        
        # Parse GraphQL query
        document = parse(query)
        
        # Calculate complexity based on:
        # - Number of fields requested
        # - Depth of nested queries
        # - Estimated result set size
        complexity = self._calculate_complexity(document, variables)
        
        if complexity > self._max_complexity:
            raise GraphQLError(
                f"Query too complex: {complexity} > {self._max_complexity}"
            )
        
        return complexity
```

### Monitoring Integration
```python
# middleware/monitoring_middleware.py
class MonitoringMiddleware:
    """Collect metrics and traces for API calls."""
    
    def __init__(self, prometheus_registry: Registry):
        self._request_count = Counter(
            "api_requests_total",
            "Total API requests",
            ["method", "endpoint", "client_id", "status"],
            registry=prometheus_registry
        )
        self._request_duration = Histogram(
            "api_request_duration_seconds",
            "API request duration",
            ["method", "endpoint", "client_id"],
            registry=prometheus_registry
        )
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Monitor API request metrics."""
        
        start_time = time.time()
        
        # Get client context
        client_id = getattr(
            request.state, "client_context", {}
        ).get("client_id", "unknown")
        
        try:
            response = await call_next(request)
            status = response.status_code
        except Exception as e:
            status = 500
            raise
        finally:
            # Record metrics
            duration = time.time() - start_time
            
            self._request_count.labels(
                method=request.method,
                endpoint=request.url.path,
                client_id=client_id,
                status=status
            ).inc()
            
            self._request_duration.labels(
                method=request.method,
                endpoint=request.url.path,
                client_id=client_id
            ).observe(duration)
        
        return response
```

## 🎯 Real-World Benefits

Esta API layer proporciona:

- **Developer Experience**: GraphQL flexibility + FastAPI documentation
- **Performance**: Query optimization and caching
- **Security**: Multi-layer authentication and client isolation
- **Monitoring**: Comprehensive metrics and tracing
- **Scalability**: Rate limiting and query complexity control

---

*La capa de API es donde la funcionalidad del sistema se hace accesible al mundo exterior de manera segura y eficiente.*
