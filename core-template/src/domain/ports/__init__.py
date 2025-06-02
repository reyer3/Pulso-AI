"""Domain ports for hexagonal architecture.

This module contains the ports (interfaces) that define contracts
between the domain layer and infrastructure layer. These interfaces
allow swapping data sources and external services without affecting
business logic.

Architecture Pattern:
    Domain Layer defines WHAT it needs (ports)
    Infrastructure Layer implements HOW to get it (adapters)

Key Benefits:
    - Client isolation: Same business logic, different data sources
    - Testability: Easy mocking with interface contracts
    - Flexibility: Swap BigQuery <-> PostgreSQL <-> MySQL transparently
    - Multi-tenancy: Different clients, same domain logic

Examples:
    >>> # Application layer uses interfaces only
    >>> class GenerateDashboardUseCase:
    ...     def __init__(
    ...         self,
    ...         cliente_repo: ClienteRepository,
    ...         gestion_repo: GestionRepository
    ...     ):
    ...         self.cliente_repo = cliente_repo
    ...         self.gestion_repo = gestion_repo
    ...
    ...     async def execute(self, filters) -> Dashboard:
    ...         clientes = await self.cliente_repo.find_clientes_en_mora()
    ...         # Business logic here using interfaces
"""

from .repositories import (
    ClienteRepository,
    GestionRepository,
    BaseRepository
)

from .services import (
    MetricaCalculatorService,
    ConfigurationService,
    NotificationService
)

from .events import (
    EventPublisher,
    DomainEvent
)

__all__ = [
    # Repositories
    "ClienteRepository",
    "GestionRepository", 
    "BaseRepository",
    
    # Services
    "MetricaCalculatorService",
    "ConfigurationService",
    "NotificationService",
    
    # Events
    "EventPublisher",
    "DomainEvent"
]
