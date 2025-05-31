"""Gestion domain entity.

Represents a collection management action performed on a customer.
This entity encapsulates business rules about contact effectiveness,
commitment tracking, and collection outcomes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

from ..value_objects.enums import CanalContacto, TipificacionHomologada


@dataclass
class Gestion:
    """Entity representing a collection management action.
    
    This entity tracks all collection activities performed on customers,
    including contact attempts, outcomes, and follow-up requirements.
    
    Examples:
        >>> from datetime import datetime
        >>> gestion = Gestion(
        ...     documento_cliente="12345678",
        ...     fecha=datetime.now(),
        ...     canal=CanalContacto.CALL,
        ...     ejecutivo="Ana García",
        ...     tipificacion_original="CONT_COMP",
        ...     tipificacion_homologada=TipificacionHomologada.COMPROMISO_PAGO,
        ...     es_contacto=True,
        ...     es_compromiso=True
        ... )
        >>> gestion.es_gestion_exitosa()
        True
        >>> gestion.requiere_seguimiento()
        True
    """
    
    documento_cliente: str  # FK to Cliente entity
    fecha: datetime  # When the management action occurred
    canal: CanalContacto  # Communication channel used
    ejecutivo: str  # Name of the executive who performed the action
    tipificacion_original: str  # Client-specific tipification
    tipificacion_homologada: TipificacionHomologada  # Standardized tipification
    es_contacto: bool  # Whether effective contact was made
    es_compromiso: bool  # Whether customer committed to payment
    id: str = None  # UUID for the management action
    observaciones: Optional[str] = None  # Additional notes
    monto_comprometido: Optional[float] = None  # Committed payment amount
    fecha_compromiso: Optional[datetime] = None  # When payment was promised
    numero_intentos: int = 1  # Number of contact attempts
    duracion_minutos: Optional[int] = None  # Duration of contact
    metadata: Optional[Dict[str, Any]] = None  # Additional client-specific data
    
    def __post_init__(self) -> None:
        """Initialize calculated fields and validate invariants."""
        if self.id is None:
            self.id = str(uuid4())
        
        # Validation rules
        if not self.documento_cliente.strip():
            raise ValueError("Documento cliente no puede estar vacío")
        if not self.ejecutivo.strip():
            raise ValueError("Ejecutivo no puede estar vacío")
        if self.numero_intentos < 1:
            raise ValueError("Número de intentos debe ser mayor a 0")
        
        # Business rule: If there's a commitment, there must be contact
        if self.es_compromiso and not self.es_contacto:
            raise ValueError("No puede haber compromiso sin contacto efectivo")
        
        # Business rule: Commitment amount should be positive if specified
        if self.monto_comprometido is not None and self.monto_comprometido <= 0:
            raise ValueError("Monto comprometido debe ser positivo")
    
    def es_gestion_exitosa(self) -> bool:
        """Determine if the management action was successful.
        
        Business rule: A management action is successful if effective
        contact was made AND customer committed to payment.
        
        Returns:
            True if management was successful
            
        Examples:
            >>> gestion = Gestion(..., es_contacto=True, es_compromiso=True)
            >>> gestion.es_gestion_exitosa()
            True
        """
        return self.es_contacto and self.es_compromiso
    
    def requiere_seguimiento(self) -> bool:
        """Determine if this management action requires follow-up.
        
        Business rule: Follow-up is required if customer committed
        to payment or if contact was made but no commitment obtained.
        
        Returns:
            True if follow-up is required
        """
        return self.es_compromiso or (
            self.es_contacto and 
            self.tipificacion_homologada not in [
                TipificacionHomologada.NO_INTERESADO,
                TipificacionHomologada.DISPUTA_DEUDA
            ]
        )
    
    def es_contacto_efectivo(self) -> bool:
        """Determine if contact was effective.
        
        Business rule: Contact is effective if customer was reached
        and conversation was meaningful (not wrong number, etc.).
        
        Returns:
            True if contact was effective
        """
        return (
            self.es_contacto and 
            self.tipificacion_homologada != TipificacionHomologada.NUMERO_ERRADO
        )
    
    def calcular_productividad_score(self) -> float:
        """Calculate productivity score for this management action.
        
        Business rule: Score based on contact success, commitment,
        and efficiency metrics.
        
        Returns:
            Productivity score between 0.0 and 1.0
        """
        score = 0.0
        
        # Base score for contact
        if self.es_contacto_efectivo():
            score += 0.4
        
        # Bonus for commitment
        if self.es_compromiso:
            score += 0.4
        
        # Efficiency bonus (fewer attempts = higher score)
        if self.numero_intentos == 1:
            score += 0.2
        elif self.numero_intentos <= 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def es_canal_digital(self) -> bool:
        """Determine if digital channel was used.
        
        Returns:
            True if channel is digital (email, SMS, WhatsApp)
        """
        return self.canal in [
            CanalContacto.EMAIL,
            CanalContacto.SMS,
            CanalContacto.WHATSAPP
        ]
    
    def tiempo_desde_gestion(self) -> int:
        """Calculate days since this management action.
        
        Returns:
            Number of days since management action
        """
        return (datetime.now() - self.fecha).days
    
    def es_compromiso_vencido(self) -> bool:
        """Check if payment commitment is overdue.
        
        Returns:
            True if commitment date has passed without payment
        """
        if not self.es_compromiso or not self.fecha_compromiso:
            return False
        
        return datetime.now() > self.fecha_compromiso
    
    def __str__(self) -> str:
        """String representation of the management action."""
        return (
            f"Gestion(cliente={self.documento_cliente}, "
            f"fecha={self.fecha.strftime('%Y-%m-%d')}, "
            f"canal={self.canal.value}, "
            f"exitosa={self.es_gestion_exitosa()})"
        )
    
    def __eq__(self, other) -> bool:
        """Equality based on ID."""
        if not isinstance(other, Gestion):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)
