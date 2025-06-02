"""Service interfaces for domain operations.

This module contains service interfaces that define contracts
for domain operations that don't naturally belong to a single
entity or require external resources.

Services vs Repositories:
- Repositories: Data access operations for specific entities
- Services: Domain operations, calculations, external integrations

Examples:
    >>> from domain.ports.services import MetricaCalculatorService
    >>> from domain.ports.services import ConfigurationService
    >>> 
    >>> class DashboardUseCase:
    ...     def __init__(
    ...         self,
    ...         metrica_service: MetricaCalculatorService,
    ...         config_service: ConfigurationService
    ...     ):
    ...         self.metrica_service = metrica_service
    ...         self.config_service = config_service
"""

from .metrica_calculator import MetricaCalculatorService
from .configuration_service import ConfigurationService
from .notification_service import NotificationService

__all__ = [
    "MetricaCalculatorService",
    "ConfigurationService",
    "NotificationService"
]
