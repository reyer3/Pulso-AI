"""Domain event definitions.

Defines domain events that represent important business occurrences
within the collection management system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4


@dataclass
class DomainEvent:
    """Base class for all domain events.
    
    Provides common structure and behavior for domain events
    in the collection management system.
    """
    
    event_id: str
    event_type: str
    timestamp: datetime
    source: str = "pulso-ai"
    version: str = "1.0"
    correlation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize calculated fields."""
        if not self.event_id:
            self.event_id = str(uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "version": self.version,
            "correlation_id": self.correlation_id,
            "metadata": self.metadata or {}
        }


@dataclass
class GestionCreatedEvent(DomainEvent):
    """Event published when a new gestion is created.
    
    Represents the creation of a collection management action,
    enabling real-time updates and downstream processing.
    """
    
    gestion_id: str
    cliente_documento: str
    ejecutivo: str
    canal: str
    tipificacion_homologada: str
    es_contacto: bool
    es_compromiso: bool
    fue_exitosa: bool
    duracion_minutos: Optional[int] = None
    monto_comprometido: Optional[float] = None
    
    def __post_init__(self):
        self.event_type = "GestionCreatedEvent"
        super().__post_init__()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with gestion-specific data."""
        base_dict = super().to_dict()
        base_dict.update({
            "gestion_id": self.gestion_id,
            "cliente_documento": self.cliente_documento,
            "ejecutivo": self.ejecutivo,
            "canal": self.canal,
            "tipificacion_homologada": self.tipificacion_homologada,
            "es_contacto": self.es_contacto,
            "es_compromiso": self.es_compromiso,
            "fue_exitosa": self.fue_exitosa,
            "duracion_minutos": self.duracion_minutos,
            "monto_comprometido": self.monto_comprometido
        })
        return base_dict


@dataclass
class ClienteUpdatedEvent(DomainEvent):
    """Event published when customer information is updated.
    
    Provides audit trail and triggers dependent processes
    when customer data changes.
    """
    
    cliente_documento: str
    campos_actualizados: list[str]
    valores_anteriores: Dict[str, Any]
    valores_nuevos: Dict[str, Any]
    usuario_actualizacion: Optional[str] = None
    
    def __post_init__(self):
        self.event_type = "ClienteUpdatedEvent"
        super().__post_init__()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with update-specific data."""
        base_dict = super().to_dict()
        base_dict.update({
            "cliente_documento": self.cliente_documento,
            "campos_actualizados": self.campos_actualizados,
            "valores_anteriores": self.valores_anteriores,
            "valores_nuevos": self.valores_nuevos,
            "usuario_actualizacion": self.usuario_actualizacion
        })
        return base_dict


@dataclass
class MetricaCalculatedEvent(DomainEvent):
    """Event published when business metrics are calculated.
    
    Enables real-time dashboard updates and performance monitoring
    when new metrics are computed.
    """
    
    metrica_nombre: str
    metrica_valor: float
    metrica_unidad: str
    ejecutivo: Optional[str] = None
    periodo: Optional[str] = None
    filtros_aplicados: Optional[Dict[str, Any]] = None
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    nivel_rendimiento: Optional[str] = None
    
    def __post_init__(self):
        self.event_type = "MetricaCalculatedEvent"
        super().__post_init__()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with metric-specific data."""
        base_dict = super().to_dict()
        base_dict.update({
            "metrica_nombre": self.metrica_nombre,
            "metrica_valor": self.metrica_valor,
            "metrica_unidad": self.metrica_unidad,
            "ejecutivo": self.ejecutivo,
            "periodo": self.periodo,
            "filtros_aplicados": self.filtros_aplicados,
            "threshold_warning": self.threshold_warning,
            "threshold_critical": self.threshold_critical,
            "nivel_rendimiento": self.nivel_rendimiento
        })
        return base_dict


@dataclass
class CommitmentOverdueEvent(DomainEvent):
    """Event published when customer payment commitment becomes overdue.
    
    Triggers follow-up processes and alerts when customers
    fail to honor payment commitments.
    """
    
    cliente_documento: str
    gestion_id: str
    fecha_compromiso: datetime
    monto_comprometido: float
    dias_vencimiento: int
    ejecutivo_original: str
    requiere_seguimiento: bool = True
    
    def __post_init__(self):
        self.event_type = "CommitmentOverdueEvent"
        super().__post_init__()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with commitment-specific data."""
        base_dict = super().to_dict()
        base_dict.update({
            "cliente_documento": self.cliente_documento,
            "gestion_id": self.gestion_id,
            "fecha_compromiso": self.fecha_compromiso.isoformat(),
            "monto_comprometido": self.monto_comprometido,
            "dias_vencimiento": self.dias_vencimiento,
            "ejecutivo_original": self.ejecutivo_original,
            "requiere_seguimiento": self.requiere_seguimiento
        })
        return base_dict


@dataclass
class SystemAlertEvent(DomainEvent):
    """Event published for system-level alerts and notifications.
    
    Used for operational monitoring, error reporting,
    and system health notifications.
    """
    
    alert_type: str
    severity: str  # info, warning, error, critical
    message: str
    component: Optional[str] = None
    client_id: Optional[str] = None
    error_code: Optional[str] = None
    
    def __post_init__(self):
        self.event_type = "SystemAlertEvent"
        super().__post_init__()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with alert-specific data."""
        base_dict = super().to_dict()
        base_dict.update({
            "alert_type": self.alert_type,
            "severity": self.severity,
            "message": self.message,
            "component": self.component,
            "client_id": self.client_id,
            "error_code": self.error_code
        })
        return base_dict


@dataclass
class DashboardGeneratedEvent(DomainEvent):
    """Event published when dashboard is successfully generated.
    
    Tracks dashboard generation for performance monitoring
    and user analytics.
    """
    
    dashboard_id: str
    client_id: str
    usuario: str
    filtros_aplicados: Dict[str, Any]
    tiempo_generacion_ms: int
    metricas_incluidas: list[str]
    
    def __post_init__(self):
        self.event_type = "DashboardGeneratedEvent"
        super().__post_init__()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with dashboard-specific data."""
        base_dict = super().to_dict()
        base_dict.update({
            "dashboard_id": self.dashboard_id,
            "client_id": self.client_id,
            "usuario": self.usuario,
            "filtros_aplicados": self.filtros_aplicados,
            "tiempo_generacion_ms": self.tiempo_generacion_ms,
            "metricas_incluidas": self.metricas_incluidas
        })
        return base_dict
