"""Event interfaces for domain event handling.

Event ports define contracts for domain event publishing and handling.
Supports event-driven architecture for loose coupling between bounded contexts.

Key Components:
    - EventPublisher: Interface for publishing domain events
    - DomainEvent: Base class for domain events
    - Event handling patterns for async processing

Benefits:
    - Decoupled communication between services
    - Audit trail for business operations
    - Integration with external systems
    - Real-time notifications and updates
"""

from .event_publisher import EventPublisher
from .domain_events import (
    DomainEvent,
    GestionCreatedEvent,
    ClienteUpdatedEvent,
    MetricaCalculatedEvent,
    CommitmentOverdueEvent
)

__all__ = [
    "EventPublisher",
    "DomainEvent",
    "GestionCreatedEvent",
    "ClienteUpdatedEvent",
    "MetricaCalculatedEvent",
    "CommitmentOverdueEvent"
]
