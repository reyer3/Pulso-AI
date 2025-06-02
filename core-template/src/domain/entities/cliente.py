"""Cliente domain entity.

Represents a customer with debt in the collection system.
This entity encapsulates business rules related to debt status,
payment capacity, and collection strategies.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Cliente:
    """Core entity representing a customer with debt.
    
    This entity contains the essential information about a customer
    and provides business methods to determine their collection status.
    
    Examples:
        >>> cliente = Cliente(
        ...     documento="12345678",
        ...     nombre="Juan Pérez",
        ...     saldo_actual=1500.50,
        ...     dias_mora=45
        ... )
        >>> cliente.esta_en_mora(30)
        True
        >>> cliente.tiene_deuda_significativa(1000.0)
        True
        >>> cliente.requiere_atencion_urgente(60, 2000.0)
        False
    """
    
    documento: str  # Primary key - identity document
    nombre: str  # Full customer name
    saldo_actual: float  # Current debt amount
    dias_mora: int  # Days overdue since last payment
    telefono: Optional[str] = None  # Primary contact phone
    email: Optional[str] = None  # Email address
    ultima_actualizacion: Optional[datetime] = None  # Last data update
    
    def __post_init__(self) -> None:
        """Validate entity invariants after initialization."""
        if not self.documento.strip():
            raise ValueError("Documento no puede estar vacío")
        if not self.nombre.strip():
            raise ValueError("Nombre no puede estar vacío")
        if self.saldo_actual < 0:
            raise ValueError("Saldo actual no puede ser negativo")
        if self.dias_mora < 0:
            raise ValueError("Días de mora no pueden ser negativos")
    
    def esta_en_mora(self, dias_minimos: int = 30) -> bool:
        """Determine if customer is overdue based on minimum days.
        
        Business rule: A customer is considered overdue if their
        days_mora exceeds the specified minimum threshold.
        
        Args:
            dias_minimos: Minimum days to consider overdue (default: 30)
            
        Returns:
            True if customer is overdue, False otherwise
            
        Examples:
            >>> cliente = Cliente("123", "Juan", 500.0, 45)
            >>> cliente.esta_en_mora(30)
            True
            >>> cliente.esta_en_mora(60)
            False
        """
        return self.dias_mora >= dias_minimos
    
    def tiene_deuda_significativa(self, monto_minimo: float = 100.0) -> bool:
        """Determine if customer has significant debt.
        
        Business rule: Debt is considered significant if it exceeds
        the minimum threshold amount.
        
        Args:
            monto_minimo: Minimum amount to consider significant
            
        Returns:
            True if debt is significant, False otherwise
            
        Examples:
            >>> cliente = Cliente("123", "Juan", 500.0, 30)
            >>> cliente.tiene_deuda_significativa(100.0)
            True
            >>> cliente.tiene_deuda_significativa(1000.0)
            False
        """
        return self.saldo_actual >= monto_minimo
    
    def requiere_atencion_urgente(
        self, 
        dias_criticos: int = 90, 
        monto_critico: float = 1000.0
    ) -> bool:
        """Determine if customer requires urgent attention.
        
        Business rule: Customer requires urgent attention if they have
        both significant debt and are critically overdue.
        
        Args:
            dias_criticos: Days threshold for critical overdue status
            monto_critico: Amount threshold for critical debt
            
        Returns:
            True if customer requires urgent attention
            
        Examples:
            >>> cliente = Cliente("123", "Juan", 1500.0, 100)
            >>> cliente.requiere_atencion_urgente(90, 1000.0)
            True
        """
        return (
            self.esta_en_mora(dias_criticos) and 
            self.tiene_deuda_significativa(monto_critico)
        )
    
    def calcular_prioridad_cobranza(self) -> str:
        """Calculate collection priority based on business rules.
        
        Business rule: Priority is determined by combination of
        debt amount and days overdue.
        
        Returns:
            Priority level: "ALTA", "MEDIA", "BAJA"
            
        Examples:
            >>> cliente = Cliente("123", "Juan", 2000.0, 120)
            >>> cliente.calcular_prioridad_cobranza()
            'ALTA'
        """
        if self.requiere_atencion_urgente(90, 1500.0):
            return "ALTA"
        elif self.esta_en_mora(30) and self.tiene_deuda_significativa(500.0):
            return "MEDIA"
        else:
            return "BAJA"
    
    def es_contactable(self) -> bool:
        """Determine if customer has contact information.
        
        Returns:
            True if customer has phone or email
        """
        return bool(self.telefono or self.email)
    
    def __str__(self) -> str:
        """String representation of the customer."""
        return f"Cliente(doc={self.documento}, nombre={self.nombre}, deuda={self.saldo_actual})"
    
    def __eq__(self, other) -> bool:
        """Equality based on document (business key)."""
        if not isinstance(other, Cliente):
            return False
        return self.documento == other.documento
    
    def __hash__(self) -> int:
        """Hash based on document (business key)."""
        return hash(self.documento)
