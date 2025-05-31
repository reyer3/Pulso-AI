"""Domain-specific exceptions.

This module defines exceptions that represent business rule violations
and domain-level errors in the debt collection system.
"""

from typing import Optional, Dict, Any


class DomainException(Exception):
    """Base exception for all domain-level errors.
    
    This is the base class for all exceptions that originate
    from the domain layer and represent business rule violations.
    
    Attributes:
        message: Human-readable error message
        code: Machine-readable error code
        context: Additional context about the error
    """
    
    def __init__(
        self, 
        message: str, 
        code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize domain exception.
        
        Args:
            message: Human-readable error description
            code: Machine-readable error code for API responses
            context: Additional context data about the error
        """
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
        self.context = context or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization.
        
        Returns:
            Dictionary representation of the exception
        """
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "context": self.context
        }


class ClienteNotFound(DomainException):
    """Exception raised when a customer cannot be found.
    
    This exception is raised when attempting to access a customer
    that doesn't exist in the system.
    
    Examples:
        >>> raise ClienteNotFound("12345678")
        ClienteNotFound: Cliente con documento 12345678 no encontrado
    """
    
    def __init__(self, documento: str) -> None:
        """Initialize customer not found exception.
        
        Args:
            documento: Customer document that was not found
        """
        message = f"Cliente con documento {documento} no encontrado"
        super().__init__(
            message=message,
            code="CLIENTE_NOT_FOUND",
            context={"documento": documento}
        )
        self.documento = documento


class GestionInvalida(DomainException):
    """Exception raised when a management action is invalid.
    
    This exception is raised when attempting to create or modify
    a management action that violates business rules.
    
    Examples:
        >>> raise GestionInvalida(
        ...     "No puede haber compromiso sin contacto efectivo",
        ...     "COMPROMISO_SIN_CONTACTO"
        ... )
    """
    
    def __init__(
        self, 
        message: str, 
        code: Optional[str] = None,
        gestion_id: Optional[str] = None
    ) -> None:
        """Initialize invalid management exception.
        
        Args:
            message: Description of the validation error
            code: Specific error code
            gestion_id: ID of the invalid management action
        """
        context = {}
        if gestion_id:
            context["gestion_id"] = gestion_id
        
        super().__init__(
            message=message,
            code=code or "GESTION_INVALIDA",
            context=context
        )
        self.gestion_id = gestion_id


class MetricaInvalida(DomainException):
    """Exception raised when a metric calculation is invalid.
    
    This exception is raised when metric values or calculations
    violate business rules or validation constraints.
    
    Examples:
        >>> raise MetricaInvalida(
        ...     "Valor de porcentaje debe estar entre 0 y 100",
        ...     "PORCENTAJE_FUERA_RANGO",
        ...     metrica_nombre="tasa_contactabilidad"
        ... )
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        metrica_nombre: Optional[str] = None,
        valor: Optional[float] = None
    ) -> None:
        """Initialize invalid metric exception.
        
        Args:
            message: Description of the validation error
            code: Specific error code
            metrica_nombre: Name of the invalid metric
            valor: Invalid value that caused the error
        """
        context = {}
        if metrica_nombre:
            context["metrica_nombre"] = metrica_nombre
        if valor is not None:
            context["valor"] = valor
        
        super().__init__(
            message=message,
            code=code or "METRICA_INVALIDA",
            context=context
        )
        self.metrica_nombre = metrica_nombre
        self.valor = valor


class HomologacionError(DomainException):
    """Exception raised when tipification homologation fails.
    
    This exception is raised when the system cannot map
    a client-specific tipification to the standard homologated value.
    
    Examples:
        >>> raise HomologacionError(
        ...     "TIPO_DESCONOCIDO",
        ...     "movistar-peru"
        ... )
    """
    
    def __init__(
        self,
        tipificacion_original: str,
        cliente_codigo: str,
        message: Optional[str] = None
    ) -> None:
        """Initialize homologation error.
        
        Args:
            tipificacion_original: Original client tipification
            cliente_codigo: Client code where error occurred
            message: Custom error message
        """
        if message is None:
            message = (
                f"No se pudo homologar tipificación '{tipificacion_original}' "
                f"para cliente '{cliente_codigo}'"
            )
        
        super().__init__(
            message=message,
            code="HOMOLOGACION_ERROR",
            context={
                "tipificacion_original": tipificacion_original,
                "cliente_codigo": cliente_codigo
            }
        )
        self.tipificacion_original = tipificacion_original
        self.cliente_codigo = cliente_codigo


class ReglaNegocioViolada(DomainException):
    """Exception raised when a business rule is violated.
    
    This is a generic exception for business rule violations
    that don't fit into more specific exception types.
    
    Examples:
        >>> raise ReglaNegocioViolada(
        ...     "No se puede procesar pago mayor al saldo actual",
        ...     "PAGO_EXCEDE_SALDO",
        ...     {"pago": 1000.0, "saldo": 500.0}
        ... )
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize business rule violation.
        
        Args:
            message: Description of the violated rule
            code: Specific rule violation code
            context: Additional context about the violation
        """
        super().__init__(
            message=message,
            code=code or "REGLA_NEGOCIO_VIOLADA",
            context=context
        )


class ConfiguracionInvalida(DomainException):
    """Exception raised when client configuration is invalid.
    
    This exception is raised when client configuration
    violates validation rules or contains inconsistent data.
    """
    
    def __init__(
        self,
        campo: str,
        valor: Any,
        razon: str
    ) -> None:
        """Initialize configuration validation error.
        
        Args:
            campo: Configuration field that is invalid
            valor: Invalid value
            razon: Reason why the value is invalid
        """
        message = f"Configuración inválida en campo '{campo}': {razon}"
        super().__init__(
            message=message,
            code="CONFIGURACION_INVALIDA",
            context={
                "campo": campo,
                "valor": valor,
                "razon": razon
            }
        )
        self.campo = campo
        self.valor = valor
        self.razon = razon


class OperacionNoPermitida(DomainException):
    """Exception raised when an operation is not allowed.
    
    This exception is raised when attempting to perform
    an operation that is not permitted given the current state.
    """
    
    def __init__(
        self,
        operacion: str,
        estado_actual: str,
        razon: Optional[str] = None
    ) -> None:
        """Initialize operation not permitted error.
        
        Args:
            operacion: Operation that was attempted
            estado_actual: Current state that prevents the operation
            razon: Additional reason why operation is not permitted
        """
        message = f"Operación '{operacion}' no permitida en estado '{estado_actual}'"
        if razon:
            message += f": {razon}"
        
        super().__init__(
            message=message,
            code="OPERACION_NO_PERMITIDA",
            context={
                "operacion": operacion,
                "estado_actual": estado_actual,
                "razon": razon
            }
        )
        self.operacion = operacion
        self.estado_actual = estado_actual
        self.razon = razon
