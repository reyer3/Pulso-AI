"""Domain enums.

Enumerations for standardized values across the multi-client system.
Provides consistent vocabulary between different clients (Movistar, Claro, Tigo).
"""

from enum import Enum


class CanalContacto(Enum):
    """Enum para canales de contacto en gestiones de cobranza.
    
    Estandariza los canales de contacto utilizados por todos los clientes,
    independientemente de cómo los nombren internamente.
    
    Values:
        CALL: Llamada telefónica directa con agente humano
        VOICEBOT: Llamada automatizada con bot de voz
        EMAIL: Correo electrónico
        SMS: Mensaje de texto
        WHATSAPP: Mensaje por WhatsApp
        VISITA_DOMICILIO: Visita presencial al domicilio
        
    Examples:
        >>> canal = CanalContacto.CALL
        >>> canal.value
        'CALL'
        >>> CanalContacto.es_canal_digital(canal)
        False
    """
    
    CALL = "CALL"
    VOICEBOT = "VOICEBOT"
    EMAIL = "EMAIL"
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"
    VISITA_DOMICILIO = "VISITA_DOMICILIO"
    
    @classmethod
    def es_canal_digital(cls, canal: 'CanalContacto') -> bool:
        """Determina si un canal es digital (no requiere presencia física).
        
        Args:
            canal: Canal de contacto a evaluar
            
        Returns:
            True si el canal es digital
            
        Examples:
            >>> CanalContacto.es_canal_digital(CanalContacto.EMAIL)
            True
            >>> CanalContacto.es_canal_digital(CanalContacto.VISITA_DOMICILIO)
            False
        """
        canales_digitales = {
            cls.VOICEBOT,
            cls.EMAIL,
            cls.SMS,
            cls.WHATSAPP
        }
        return canal in canales_digitales
    
    @classmethod
    def es_canal_sincronico(cls, canal: 'CanalContacto') -> bool:
        """Determina si un canal permite comunicación en tiempo real.
        
        Args:
            canal: Canal de contacto a evaluar
            
        Returns:
            True si el canal es síncrono
        """
        canales_sincronos = {
            cls.CALL,
            cls.VOICEBOT,
            cls.WHATSAPP,  # Puede ser síncrono
            cls.VISITA_DOMICILIO
        }
        return canal in canales_sincronos
    
    @classmethod
    def obtener_canales_automatizados(cls) -> set['CanalContacto']:
        """Retorna canales que no requieren intervención humana.
        
        Returns:
            Set de canales automatizados
        """
        return {
            cls.VOICEBOT,
            cls.EMAIL,
            cls.SMS
        }


class TipificacionHomologada(Enum):
    """Enum para tipificaciones homologadas cross-client.
    
    Estandariza las tipificaciones de gestión entre diferentes clientes.
    Cada cliente puede tener sus propias tipificaciones internas que se
    mapean a estas tipificaciones homologadas.
    
    Mapping examples:
    - Movistar: "CONT_COMP" -> COMPROMISO_PAGO
    - Claro: "CONTACTO_COMPROMISO" -> COMPROMISO_PAGO  
    - Tigo: "COMP_PAGO" -> COMPROMISO_PAGO
    
    Values:
        CONTACTO_EFECTIVO: Se logró contactar al cliente
        COMPROMISO_PAGO: Cliente comprometió realizar pago
        NO_CONTACTO: No se pudo contactar al cliente
        NUMERO_ERRADO: Número telefónico incorrecto o inexistente
        NO_INTERESADO: Cliente no muestra interés en resolver deuda
        DISPUTA_DEUDA: Cliente disputa la validez de la deuda
        FALLECIDO: Cliente fallecido (requiere proceso especial)
        REFINANCIACION: Cliente solicita refinanciamiento
        
    Examples:
        >>> tip = TipificacionHomologada.COMPROMISO_PAGO
        >>> TipificacionHomologada.es_resultado_positivo(tip)
        True
    """
    
    CONTACTO_EFECTIVO = "CONTACTO_EFECTIVO"
    COMPROMISO_PAGO = "COMPROMISO_PAGO"
    NO_CONTACTO = "NO_CONTACTO"
    NUMERO_ERRADO = "NUMERO_ERRADO"
    NO_INTERESADO = "NO_INTERESADO"
    DISPUTA_DEUDA = "DISPUTA_DEUDA"
    FALLECIDO = "FALLECIDO"
    REFINANCIACION = "REFINANCIACION"
    
    @classmethod
    def es_resultado_positivo(cls, tipificacion: 'TipificacionHomologada') -> bool:
        """Determina si una tipificación representa resultado positivo.
        
        Args:
            tipificacion: Tipificación a evaluar
            
        Returns:
            True si la tipificación es considerada positiva
            
        Examples:
            >>> TipificacionHomologada.es_resultado_positivo(
            ...     TipificacionHomologada.COMPROMISO_PAGO
            ... )
            True
            >>> TipificacionHomologada.es_resultado_positivo(
            ...     TipificacionHomologada.NO_CONTACTO
            ... )
            False
        """
        resultados_positivos = {
            cls.CONTACTO_EFECTIVO,
            cls.COMPROMISO_PAGO,
            cls.REFINANCIACION
        }
        return tipificacion in resultados_positivos
    
    @classmethod
    def requiere_seguimiento(cls, tipificacion: 'TipificacionHomologada') -> bool:
        """Determina si tipificación requiere seguimiento posterior.
        
        Args:
            tipificacion: Tipificación a evaluar
            
        Returns:
            True si requiere seguimiento
        """
        requieren_seguimiento = {
            cls.CONTACTO_EFECTIVO,  # Contacto sin compromiso
            cls.NO_CONTACTO,        # Reintentar contacto
            cls.DISPUTA_DEUDA      # Proceso de resolución
        }
        return tipificacion in requieren_seguimiento
    
    @classmethod
    def es_caso_especial(cls, tipificacion: 'TipificacionHomologada') -> bool:
        """Determina si tipificación requiere manejo especial.
        
        Args:
            tipificacion: Tipificación a evaluar
            
        Returns:
            True si requiere proceso especial
        """
        casos_especiales = {
            cls.FALLECIDO,          # Proceso legal especial
            cls.DISPUTA_DEUDA,      # Proceso de validación
            cls.REFINANCIACION      # Proceso comercial
        }
        return tipificacion in casos_especiales
    
    @classmethod
    def obtener_tipificaciones_contacto(cls) -> set['TipificacionHomologada']:
        """Retorna tipificaciones que indican contacto exitoso.
        
        Returns:
            Set de tipificaciones de contacto
        """
        return {
            cls.CONTACTO_EFECTIVO,
            cls.COMPROMISO_PAGO,
            cls.NO_INTERESADO,
            cls.DISPUTA_DEUDA,
            cls.REFINANCIACION
        }
