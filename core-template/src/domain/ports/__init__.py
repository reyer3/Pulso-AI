"""Domain ports package.

This module contains the interfaces (ports) that define contracts
between the domain layer and infrastructure layer following the
hexagonal architecture pattern.

Ports vs Adapters:
- Ports (this module): Interfaces defined by domain, used by application layer
- Adapters (infrastructure): Concrete implementations of these interfaces

Example:
    >>> from domain.ports.repositories import ClienteRepository
    >>> from domain.ports.services import MetricaCalculatorService
    >>> 
    >>> # Domain uses interfaces, not concrete implementations
    >>> class GenerateDashboardUseCase:
    ...     def __init__(self, cliente_repo: ClienteRepository):
    ...         self.cliente_repo = cliente_repo
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
