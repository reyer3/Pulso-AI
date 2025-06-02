"""Event publisher interface.

Defines contracts for publishing domain events to enable
event-driven architecture and loose coupling between services.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from .domain_events import DomainEvent


class EventPublisher(ABC):
    """Interface for publishing domain events.
    
    This interface enables event-driven architecture by providing
    a contract for publishing events that occur within the domain.
    
    Key Features:
        - Async event publishing
        - Multiple event types support
        - Event metadata and context
        - Delivery guarantees through interface contract
    
    Examples:
        >>> # Publish single event
        >>> event = GestionCreatedEvent(
        ...     gestion_id="gest_123",
        ...     cliente_documento="12345678",
        ...     ejecutivo="Ana García"
        ... )
        >>> await publisher.publish_event(event)
        >>> 
        >>> # Publish multiple events in batch
        >>> events = [event1, event2, event3]
        >>> await publisher.publish_events(events)
    """
    
    @abstractmethod
    async def publish_event(self, event: DomainEvent) -> bool:
        """Publish single domain event.
        
        Publishes a domain event to the configured event system
        (message queue, event bus, webhook, etc.).
        
        Args:
            event: Domain event to publish
            
        Returns:
            True if event was successfully published
            
        Raises:
            EventPublishError: If publishing fails
            
        Examples:
            >>> from datetime import datetime
            >>> event = GestionCreatedEvent(
            ...     event_id="evt_123",
            ...     timestamp=datetime.now(),
            ...     gestion_id="gest_456",
            ...     cliente_documento="12345678",
            ...     ejecutivo="Ana García",
            ...     canal="CALL",
            ...     fue_exitosa=True
            ... )
            >>> success = await publisher.publish_event(event)
            >>> assert success
        """
        pass
    
    @abstractmethod
    async def publish_events(self, events: List[DomainEvent]) -> bool:
        """Publish multiple domain events in batch.
        
        Publishes multiple events efficiently, potentially
        using batch operations for better performance.
        
        Args:
            events: List of domain events to publish
            
        Returns:
            True if all events were successfully published
            
        Examples:
            >>> events = [
            ...     GestionCreatedEvent(...),
            ...     ClienteUpdatedEvent(...),
            ...     MetricaCalculatedEvent(...)
            ... ]
            >>> success = await publisher.publish_events(events)
        """
        pass
    
    @abstractmethod
    async def publish_gestion_created(
        self, 
        gestion_id: str,
        cliente_documento: str,
        ejecutivo: str,
        canal: str,
        fue_exitosa: bool,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Publish gestion created event.
        
        Convenience method for publishing collection management
        action created events with relevant business context.
        
        Args:
            gestion_id: Unique gestion identifier
            cliente_documento: Customer document
            ejecutivo: Agent who performed action
            canal: Communication channel used
            fue_exitosa: Whether action was successful
            metadata: Additional event context
            
        Returns:
            True if event published successfully
            
        Business Impact:
            - Triggers real-time dashboard updates
            - Updates productivity metrics
            - Sends notifications if needed
            - Feeds analytics systems
            
        Examples:
            >>> # Successful call result
            >>> await publisher.publish_gestion_created(
            ...     gestion_id="gest_789",
            ...     cliente_documento="87654321",
            ...     ejecutivo="Carlos López",
            ...     canal="CALL",
            ...     fue_exitosa=True,
            ...     metadata={"duracion_minutos": 12, "compromiso_monto": 500.0}
            ... )
        """
        pass
    
    @abstractmethod
    async def publish_cliente_updated(
        self,
        cliente_documento: str,
        campos_actualizados: List[str],
        valores_anteriores: Dict[str, Any],
        valores_nuevos: Dict[str, Any]
    ) -> bool:
        """Publish cliente updated event.
        
        Publishes event when customer information is updated,
        providing audit trail and triggering dependent processes.
        
        Args:
            cliente_documento: Customer document
            campos_actualizados: List of updated field names
            valores_anteriores: Previous field values
            valores_nuevos: New field values
            
        Returns:
            True if event published successfully
            
        Examples:
            >>> # Customer contact info updated
            >>> await publisher.publish_cliente_updated(
            ...     cliente_documento="12345678",
            ...     campos_actualizados=["telefono", "email"],
            ...     valores_anteriores={"telefono": "555-1234", "email": None},
            ...     valores_nuevos={"telefono": "555-5678", "email": "cliente@email.com"}
            ... )
        """
        pass
    
    @abstractmethod
    async def publish_metrica_calculated(
        self,
        metrica_nombre: str,
        metrica_valor: float,
        ejecutivo: Optional[str] = None,
        periodo: Optional[str] = None,
        filtros_aplicados: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Publish metric calculated event.
        
        Publishes event when business metrics are calculated,
        enabling real-time dashboard updates and notifications.
        
        Args:
            metrica_nombre: Name of calculated metric
            metrica_valor: Calculated metric value
            ejecutivo: Agent filter if metric is agent-specific
            periodo: Time period for calculation
            filtros_aplicados: Filters used in calculation
            
        Returns:
            True if event published successfully
            
        Examples:
            >>> # Daily contact rate calculated
            >>> await publisher.publish_metrica_calculated(
            ...     metrica_nombre="tasa_contactabilidad",
            ...     metrica_valor=78.5,
            ...     ejecutivo="Ana García",
            ...     periodo="daily",
            ...     filtros_aplicados={"fecha": "2024-06-01"}
            ... )
        """
        pass
    
    @abstractmethod
    async def publish_commitment_overdue(
        self,
        cliente_documento: str,
        gestion_id: str,
        fecha_compromiso: datetime,
        monto_comprometido: float,
        dias_vencimiento: int
    ) -> bool:
        """Publish commitment overdue event.
        
        Publishes event when customer payment commitment
        becomes overdue, triggering follow-up processes.
        
        Args:
            cliente_documento: Customer document
            gestion_id: Original gestion that created commitment
            fecha_compromiso: Original commitment date
            monto_comprometido: Committed payment amount
            dias_vencimiento: Days overdue
            
        Returns:
            True if event published successfully
            
        Business Impact:
            - Triggers automatic follow-up scheduling
            - Updates customer priority
            - Sends alerts to supervisors
            - Affects agent performance metrics
            
        Examples:
            >>> # Payment commitment 3 days overdue
            >>> await publisher.publish_commitment_overdue(
            ...     cliente_documento="12345678",
            ...     gestion_id="gest_456",
            ...     fecha_compromiso=datetime(2024, 5, 28),
            ...     monto_comprometido=1500.0,
            ...     dias_vencimiento=3
            ... )
        """
        pass
    
    @abstractmethod
    async def publish_system_event(
        self,
        event_type: str,
        message: str,
        severity: str = "info",
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Publish system-level event.
        
        Publishes system events for monitoring, logging,
        and operational awareness.
        
        Args:
            event_type: Type of system event
            message: Event message
            severity: Event severity (info, warning, error, critical)
            metadata: Additional event context
            
        Returns:
            True if event published successfully
            
        System Event Types:
            - "etl_completed": Data ETL process finished
            - "dashboard_generated": Dashboard successfully created
            - "alert_triggered": Automatic alert sent
            - "performance_threshold_exceeded": Metric threshold crossed
            
        Examples:
            >>> # ETL completion event
            >>> await publisher.publish_system_event(
            ...     event_type="etl_completed",
            ...     message="Daily ETL completed successfully for movistar-peru",
            ...     severity="info",
            ...     metadata={
            ...         "client_id": "movistar-peru",
            ...         "records_processed": 15420,
            ...         "duration_seconds": 45
            ...     }
            ... )
        """
        pass
    
    @abstractmethod
    async def get_event_history(
        self,
        event_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get published event history.
        
        Retrieves history of published events for debugging,
        auditing, and monitoring purposes.
        
        Args:
            event_type: Filter by event type
            start_time: Filter by publish time
            limit: Maximum results
            
        Returns:
            List of event history records
            
        Examples:
            >>> # Recent gestion events
            >>> history = await publisher.get_event_history(
            ...     event_type="GestionCreatedEvent",
            ...     start_time=datetime.now() - timedelta(hours=1)
            ... )
        """
        pass
