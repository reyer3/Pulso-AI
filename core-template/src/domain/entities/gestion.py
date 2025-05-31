"""Gestion domain entity.

Entity representing a collection management action performed on a customer.
Supports cross-client tipificacion homologation and business rules.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import uuid4

from ..value_objects.enums import CanalContacto, TipificacionHomologada


@dataclass
class Gestion:
    """Entidad que representa una gestión de cobranza.
    
    Esta entidad maneja las acciones de cobranza realizadas sobre clientes,
    incluyendo la homologación de tipificaciones entre diferentes clientes
    (Movistar usa "CONT_COMP", Claro usa "CONTACTO_COMPROMISO", etc.)
    
    Attributes:
        id: Identificador único de la gestión (UUID)
        documento_cliente: Documento del cliente gestionado (FK)
        fecha: Timestamp de cuando se realizó la gestión
        canal: Canal utilizado para el contacto
        ejecutivo: Nombre del ejecutivo que realizó la gestión
        tipificacion_original: Tipificación específica del cliente
        tipificacion_homologada: Tipificación standardizada cross-client
        es_contacto: Si se logró contacto efectivo con el cliente
        es_compromiso: Si el cliente comprometió realizar pago
        observaciones: Notas adicionales de la gestión
    
    Examples:
        >>> from datetime import datetime
        >>> gestion = Gestion(
        ...     documento_cliente="12345678",
        ...     fecha=datetime.now(),
        ...     canal=CanalContacto.CALL,
        ...     ejecutivo="Ana García",
        ...     tipificacion_original="CONT_COMP",  # Específico Movistar
        ...     tipificacion_homologada=TipificacionHomologada.COMPROMISO_PAGO.value,
        ...     es_contacto=True,
        ...     es_compromiso=True
        ... )
        >>> gestion.es_gestion_exitosa()
        True
    """
    
    documento_cliente: str
    fecha: datetime
    canal: CanalContacto
    ejecutivo: str
    tipificacion_original: str
    tipificacion_homologada: str
    es_contacto: bool
    es_compromiso: bool
    id: str = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        """Generate ID and validate entity constraints."""
        if self.id is None:
            self.id = str(uuid4())
            
        if not self.documento_cliente or not self.documento_cliente.strip():
            raise ValueError("El documento del cliente no puede estar vacío")
            
        if not self.ejecutivo or not self.ejecutivo.strip():
            raise ValueError("El ejecutivo no puede estar vacío")
            
        if not self.tipificacion_original or not self.tipificacion_original.strip():
            raise ValueError("La tipificación original no puede estar vacía")
            
        if not self.tipificacion_homologada or not self.tipificacion_homologada.strip():
            raise ValueError("La tipificación homologada no puede estar vacía")
            
        # Validate tipificacion_homologada is a valid enum value
        valid_tipificaciones = [t.value for t in TipificacionHomologada]
        if self.tipificacion_homologada not in valid_tipificaciones:
            raise ValueError(
                f"Tipificación homologada inválida: {self.tipificacion_homologada}. "
                f"Válidas: {valid_tipificaciones}"
            )
    
    def es_gestion_exitosa(self) -> bool:
        """Business rule: gestión exitosa si hay contacto y compromiso.
        
        Returns:
            True si la gestión logró contacto efectivo y compromiso de pago
            
        Examples:
            >>> gestion = Gestion(
            ...     documento_cliente="12345",
            ...     fecha=datetime.now(),
            ...     canal=CanalContacto.CALL,
            ...     ejecutivo="Ana",
            ...     tipificacion_original="CONT_COMP",
            ...     tipificacion_homologada=TipificacionHomologada.COMPROMISO_PAGO.value,
            ...     es_contacto=True,
            ...     es_compromiso=True
            ... )
            >>> gestion.es_gestion_exitosa()
            True
        """
        return self.es_contacto and self.es_compromiso
    
    def es_contacto_efectivo(self) -> bool:
        """Business rule: contacto efectivo independiente de compromiso.
        
        Returns:
            True si se logró contactar al cliente, sin importar resultado
        """
        return self.es_contacto
    
    def requiere_seguimiento(self) -> bool:
        """Business rule: determina si gestión requiere seguimiento.
        
        Returns:
            True si hubo contacto pero no compromiso (requiere follow-up)
        """
        return self.es_contacto and not self.es_compromiso
    
    def es_canal_automatizado(self) -> bool:
        """Business rule: determina si el canal es automatizado.
        
        Returns:
            True si el canal no requiere intervención humana directa
        """
        canales_automatizados = {
            CanalContacto.VOICEBOT,
            CanalContacto.EMAIL,
            CanalContacto.SMS,
            CanalContacto.WHATSAPP
        }
        return self.canal in canales_automatizados
    
    def obtener_efectividad_canal(self) -> str:
        """Business rule: clasifica efectividad según canal y resultado.
        
        Returns:
            Clasificación de efectividad: "ALTA", "MEDIA", "BAJA"
        """
        if self.es_gestion_exitosa():
            return "ALTA"
        elif self.es_contacto_efectivo():
            return "MEDIA" 
        else:
            return "BAJA"
