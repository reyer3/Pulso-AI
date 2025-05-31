"""Cliente domain entity.

Core entity representing a customer with debt in the collection system.
Supports multi-client scenarios with universal business rules.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    """Entidad core que representa un cliente con deuda.
    
    Esta entidad es agnóstica al cliente específico (Movistar, Claro, Tigo)
    y contiene las business rules universales para el dominio de cobranza.
    
    Attributes:
        documento: Documento de identidad único (primary key)
        nombre: Nombre completo del cliente
        saldo_actual: Monto de deuda actual en moneda local
        dias_mora: Días transcurridos desde último pago
        telefono: Número de teléfono principal (opcional)
        email: Correo electrónico (opcional)
    
    Examples:
        >>> cliente = Cliente(
        ...     documento="12345678",
        ...     nombre="Juan Pérez",
        ...     saldo_actual=500.0,
        ...     dias_mora=45
        ... )
        >>> cliente.esta_en_mora(30)
        True
        >>> cliente.tiene_deuda_significativa(100.0)
        True
    """
    
    documento: str
    nombre: str
    saldo_actual: float
    dias_mora: int
    telefono: Optional[str] = None
    email: Optional[str] = None
    
    def __post_init__(self):
        """Validate entity constraints after initialization."""
        if not self.documento or not self.documento.strip():
            raise ValueError("El documento no puede estar vacío")
        
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
            
        if self.saldo_actual < 0:
            raise ValueError("El saldo actual no puede ser negativo")
            
        if self.dias_mora < 0:
            raise ValueError("Los días de mora no pueden ser negativos")
    
    def esta_en_mora(self, dias_minimos: int = 30) -> bool:
        """Business rule: determina si cliente está en mora.
        
        Args:
            dias_minimos: Umbral mínimo de días para considerar mora
            
        Returns:
            True si el cliente está en mora según el umbral
            
        Examples:
            >>> cliente = Cliente("12345", "Juan", 100.0, 45)
            >>> cliente.esta_en_mora(30)
            True
            >>> cliente.esta_en_mora(60)
            False
        """
        return self.dias_mora >= dias_minimos
    
    def tiene_deuda_significativa(self, monto_minimo: float = 100.0) -> bool:
        """Business rule: determina si deuda es significativa.
        
        Args:
            monto_minimo: Umbral mínimo para considerar deuda significativa
            
        Returns:
            True si la deuda supera el umbral mínimo
            
        Examples:
            >>> cliente = Cliente("12345", "Juan", 500.0, 30)
            >>> cliente.tiene_deuda_significativa(100.0)
            True
            >>> cliente.tiene_deuda_significativa(1000.0)
            False
        """
        return self.saldo_actual >= monto_minimo
    
    def es_cliente_prioritario(self, dias_mora_criticos: int = 90, 
                              monto_critico: float = 1000.0) -> bool:
        """Business rule: determina si es cliente prioritario para gestión.
        
        Args:
            dias_mora_criticos: Días de mora que hacen crítico el caso
            monto_critico: Monto que hace crítico el caso
            
        Returns:
            True si el cliente requiere atención prioritaria
            
        Examples:
            >>> cliente = Cliente("12345", "Juan", 1500.0, 95)
            >>> cliente.es_cliente_prioritario()
            True
        """
        return (
            self.esta_en_mora(dias_mora_criticos) or 
            self.tiene_deuda_significativa(monto_critico)
        )
    
    def puede_ser_contactado(self) -> bool:
        """Business rule: determina si cliente puede ser contactado.
        
        Returns:
            True si tiene al menos un medio de contacto disponible
        """
        return bool(self.telefono and self.telefono.strip()) or bool(
            self.email and self.email.strip()
        )
