"""Service interfaces for business operations.

Service ports define contracts for complex business operations
that don't fit naturally into entity repositories. These services
handle cross-cutting concerns and advanced business logic.

Key Services:
    - MetricaCalculatorService: Dynamic metric calculations
    - ConfigurationService: Multi-client configuration management
    - NotificationService: Alerts and notifications

Architecture Benefits:
    - Business logic centralization
    - Client-specific customization via configuration
    - Easy testing with mock implementations
    - Performance optimization through service interfaces
"""

from .metrica_calculator_service import MetricaCalculatorService
from .configuration_service import ConfigurationService
from .notification_service import NotificationService

__all__ = [
    "MetricaCalculatorService",
    "ConfigurationService",
    "NotificationService"
]
