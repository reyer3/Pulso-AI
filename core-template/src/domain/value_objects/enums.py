"""Domain enums for standardized values.

This module contains enums that define standardized values
used across different clients while maintaining consistency.
"""

from enum import Enum


class CanalContacto(Enum):
    """Communication channels used for customer contact.
    
    These channels are standardized across all clients,
    though the specific implementation may vary.
    
    Examples:
        >>> canal = CanalContacto.CALL
        >>> canal.es_canal_directo()
        True
        >>> canal.es_canal_digital()
        False
    """
    
    CALL = "CALL"  # Phone call
    VOICEBOT = "VOICEBOT"  # Automated voice system
    EMAIL = "EMAIL"  # Email communication
    SMS = "SMS"  # Text message
    WHATSAPP = "WHATSAPP"  # WhatsApp messaging
    VISITA_DOMICILIO = "VISITA_DOMICILIO"  # Home visit
    CARTA = "CARTA"  # Physical letter
    CALL_CENTER = "CALL_CENTER"  # Call center outbound
    
    def es_canal_directo(self) -> bool:
        """Check if channel allows direct conversation.
        
        Returns:
            True for channels that allow real-time conversation
        """
        return self in [self.CALL, self.WHATSAPP, self.VISITA_DOMICILIO]
    
    def es_canal_digital(self) -> bool:
        """Check if channel is digital.
        
        Returns:
            True for digital communication channels
        """
        return self in [
            self.EMAIL, 
            self.SMS, 
            self.WHATSAPP, 
            self.VOICEBOT
        ]
    
    def es_canal_automatizado(self) -> bool:
        """Check if channel is automated.
        
        Returns:
            True for automated channels (no human agent)
        """
        return self in [self.VOICEBOT, self.SMS]  # SMS can be automated
    
    def requiere_agente_humano(self) -> bool:
        """Check if channel requires human agent.
        
        Returns:
            True if human agent is required
        """
        return self in [
            self.CALL,
            self.WHATSAPP, 
            self.VISITA_DOMICILIO,
            self.CALL_CENTER
        ]
    
    @classmethod
    def canales_de_alta_conversion(cls) -> list['CanalContacto']:
        """Get channels with typically high conversion rates.
        
        Returns:
            List of high-conversion channels
        """
        return [cls.CALL, cls.WHATSAPP, cls.VISITA_DOMICILIO]
    
    @classmethod
    def canales_de_bajo_costo(cls) -> list['CanalContacto']:
        """Get low-cost communication channels.
        
        Returns:
            List of cost-effective channels
        """
        return [cls.EMAIL, cls.SMS, cls.VOICEBOT]


class TipificacionHomologada(Enum):
    """Standardized tipification across all clients.
    
    This enum provides a unified vocabulary for collection outcomes,
    regardless of how each client originally classifies them.
    
    The homologation process maps client-specific tipifications
    to these standard values.
    
    Examples:
        Movistar: "CONT_COMP" -> TipificacionHomologada.COMPROMISO_PAGO
        Claro: "PROMESA_PAGO" -> TipificacionHomologada.COMPROMISO_PAGO
        Tigo: "ACEPTA_PAGAR" -> TipificacionHomologada.COMPROMISO_PAGO
    """
    
    # Successful outcomes
    CONTACTO_EFECTIVO = "CONTACTO_EFECTIVO"  # Contact made, conversation held
    COMPROMISO_PAGO = "COMPROMISO_PAGO"  # Customer committed to payment
    PAGO_INMEDIATO = "PAGO_INMEDIATO"  # Payment made during contact
    ACUERDO_PAGO = "ACUERDO_PAGO"  # Payment plan agreed
    
    # Contact attempts without success
    NO_CONTACTO = "NO_CONTACTO"  # No answer, busy, etc.
    NUMERO_ERRADO = "NUMERO_ERRADO"  # Wrong number
    TELEFONO_APAGADO = "TELEFONO_APAGADO"  # Phone turned off
    BUZON_VOZ = "BUZON_VOZ"  # Voicemail
    
    # Contact made but no commitment
    NO_INTERESADO = "NO_INTERESADO"  # Customer refuses to pay
    SIN_CAPACIDAD_PAGO = "SIN_CAPACIDAD_PAGO"  # Customer cannot pay
    SOLICITA_FACILIDADES = "SOLICITA_FACILIDADES"  # Requests payment plan
    
    # Special cases
    DISPUTA_DEUDA = "DISPUTA_DEUDA"  # Customer disputes the debt
    FALLECIDO = "FALLECIDO"  # Customer deceased
    CAMBIO_DATOS = "CAMBIO_DATOS"  # Contact info needs update
    RECLAMO_CLIENTE = "RECLAMO_CLIENTE"  # Customer complaint
    
    def es_resultado_positivo(self) -> bool:
        """Check if tipification represents positive outcome.
        
        Returns:
            True for outcomes that advance collection process
        """
        return self in [
            self.CONTACTO_EFECTIVO,
            self.COMPROMISO_PAGO,
            self.PAGO_INMEDIATO,
            self.ACUERDO_PAGO,
            self.SOLICITA_FACILIDADES
        ]
    
    def indica_contacto_efectivo(self) -> bool:
        """Check if tipification indicates effective contact.
        
        Returns:
            True if customer was actually reached
        """
        return self not in [
            self.NO_CONTACTO,
            self.NUMERO_ERRADO,
            self.TELEFONO_APAGADO,
            self.BUZON_VOZ
        ]
    
    def requiere_seguimiento(self) -> bool:
        """Check if tipification requires follow-up action.
        
        Returns:
            True if follow-up is needed
        """
        return self in [
            self.COMPROMISO_PAGO,
            self.ACUERDO_PAGO,
            self.SOLICITA_FACILIDADES,
            self.CAMBIO_DATOS,
            self.RECLAMO_CLIENTE
        ]
    
    def es_caso_especial(self) -> bool:
        """Check if tipification is a special case.
        
        Returns:
            True for cases requiring special handling
        """
        return self in [
            self.DISPUTA_DEUDA,
            self.FALLECIDO,
            self.RECLAMO_CLIENTE
        ]
    
    @classmethod
    def tipificaciones_de_exito(cls) -> list['TipificacionHomologada']:
        """Get tipifications considered successful.
        
        Returns:
            List of successful outcome tipifications
        """
        return [
            cls.COMPROMISO_PAGO,
            cls.PAGO_INMEDIATO,
            cls.ACUERDO_PAGO
        ]
    
    @classmethod
    def tipificaciones_de_contacto(cls) -> list['TipificacionHomologada']:
        """Get tipifications that indicate contact was made.
        
        Returns:
            List of contact-indicating tipifications
        """
        return [
            tip for tip in cls 
            if tip.indica_contacto_efectivo()
        ]


class EstadoCliente(Enum):
    """Customer status in the collection process."""
    
    ACTIVO = "ACTIVO"  # Active in collection
    INACTIVO = "INACTIVO"  # Temporarily inactive
    EXCLUIDO = "EXCLUIDO"  # Excluded from collection
    JURIDICO = "JURIDICO"  # Sent to legal process
    PAGADO = "PAGADO"  # Debt fully paid
    CASTIGADO = "CASTIGADO"  # Debt written off


class PrioridadCobranza(Enum):
    """Collection priority levels."""
    
    ALTA = "ALTA"  # High priority
    MEDIA = "MEDIA"  # Medium priority
    BAJA = "BAJA"  # Low priority
    CRITICA = "CRITICA"  # Critical priority
    
    def nivel_numerico(self) -> int:
        """Get numeric priority level.
        
        Returns:
            Numeric priority (higher = more urgent)
        """
        mapping = {
            self.CRITICA: 4,
            self.ALTA: 3,
            self.MEDIA: 2,
            self.BAJA: 1
        }
        return mapping[self]
