"""Domain-specific exceptions.

Exceptions that represent business rule violations or domain invariant failures.
These are part of the ubiquitous language and should be meaningful to business stakeholders.
"""


class DomainValidationError(Exception):
    """Base exception for domain validation failures.
    
    Raised when domain entities or value objects violate business rules
    or invariants during creation or modification.
    
    Attributes:
        message: Human-readable error description
        entity_type: Type of domain entity that failed validation
        field: Specific field that caused the validation failure
    
    Examples:
        >>> raise DomainValidationError(
        ...     "El saldo no puede ser negativo",
        ...     entity_type="Cliente",
        ...     field="saldo_actual"
        ... )
    """
    
    def __init__(self, message: str, entity_type: str = None, field: str = None):
        super().__init__(message)
        self.message = message
        self.entity_type = entity_type
        self.field = field
        
    def __str__(self):
        if self.entity_type and self.field:
            return f"{self.entity_type}.{self.field}: {self.message}"
        elif self.entity_type:
            return f"{self.entity_type}: {self.message}"
        else:
            return self.message


class ClienteNotFound(DomainValidationError):
    """Exception raised when a cliente is not found.
    
    Raised during business operations that require an existing cliente
    but the documento provided doesn't match any cliente in the system.
    
    Attributes:
        documento: Document identifier that was not found
        
    Examples:
        >>> raise ClienteNotFound("12345678")
    """
    
    def __init__(self, documento: str):
        self.documento = documento
        message = f"Cliente con documento '{documento}' no encontrado"
        super().__init__(message, entity_type="Cliente", field="documento")


class GestionInvalida(DomainValidationError):
    """Exception raised when gestion data violates business rules.
    
    Raised when trying to create or modify a gestion with invalid data
    or when the gestion violates domain business rules.
    
    Attributes:
        gestion_id: ID of the invalid gestion
        violation: Specific business rule that was violated
        
    Examples:
        >>> raise GestionInvalida(
        ...     gestion_id="123",
        ...     violation="No se puede registrar compromiso sin contacto"
        ... )
    """
    
    def __init__(self, gestion_id: str = None, violation: str = None):
        self.gestion_id = gestion_id
        self.violation = violation
        
        if violation:
            message = violation
        else:
            message = "Datos de gestión inválidos"
            
        if gestion_id:
            message = f"Gestión {gestion_id}: {message}"
            
        super().__init__(message, entity_type="Gestion")


class MetricaCalculationError(DomainValidationError):
    """Exception raised when metric calculation fails.
    
    Raised when there's an error calculating a domain metric,
    either due to invalid data or mathematical errors.
    
    Attributes:
        metrica_nombre: Name of the metric that failed
        calculation_error: Specific calculation error description
        
    Examples:
        >>> raise MetricaCalculationError(
        ...     metrica_nombre="tasa_contactabilidad",
        ...     calculation_error="División por cero: no hay gestiones"
        ... )
    """
    
    def __init__(self, metrica_nombre: str, calculation_error: str = None):
        self.metrica_nombre = metrica_nombre
        self.calculation_error = calculation_error
        
        if calculation_error:
            message = f"Error calculando '{metrica_nombre}': {calculation_error}"
        else:
            message = f"Error calculando métrica '{metrica_nombre}'"
            
        super().__init__(message, entity_type="Metrica", field="valor")


class TipificacionHomologacionError(DomainValidationError):
    """Exception raised when tipificacion homologation fails.
    
    Raised when the system cannot map a client-specific tipificacion
    to a standardized homologated tipificacion.
    
    Attributes:
        tipificacion_original: Original client-specific tipificacion
        cliente_id: ID of the client whose tipificacion failed
        
    Examples:
        >>> raise TipificacionHomologacionError(
        ...     tipificacion_original="UNKNOWN_TIP",
        ...     cliente_id="movistar-peru"
        ... )
    """
    
    def __init__(self, tipificacion_original: str, cliente_id: str = None):
        self.tipificacion_original = tipificacion_original
        self.cliente_id = cliente_id
        
        message = f"No se pudo homologar tipificación '{tipificacion_original}'"
        if cliente_id:
            message += f" para cliente '{cliente_id}'"
            
        super().__init__(message, entity_type="Gestion", field="tipificacion_homologada")


class DocumentoInvalidoError(DomainValidationError):
    """Exception raised when documento format is invalid.
    
    Raised when a document identifier doesn't meet the format
    requirements for its type and country.
    
    Attributes:
        documento: Invalid document number
        tipo: Document type (DNI, CC, etc.)
        pais: Country code
        
    Examples:
        >>> raise DocumentoInvalidoError(
        ...     documento="abc123",
        ...     tipo="DNI",
        ...     pais="PE"
        ... )
    """
    
    def __init__(self, documento: str, tipo: str = None, pais: str = None):
        self.documento = documento
        self.tipo = tipo
        self.pais = pais
        
        message = f"Formato de documento inválido: '{documento}'"
        if tipo and pais:
            message += f" para tipo '{tipo}' en país '{pais}'"
            
        super().__init__(message, entity_type="DocumentoIdentidad", field="numero")


class BusinessRuleViolation(DomainValidationError):
    """Exception raised when a domain business rule is violated.
    
    Generic exception for business rule violations that don't fit
    into more specific exception categories.
    
    Attributes:
        rule_name: Name of the business rule that was violated
        context: Additional context about the violation
        
    Examples:
        >>> raise BusinessRuleViolation(
        ...     "Cliente debe tener al menos un medio de contacto",
        ...     rule_name="ContactabilityRule",
        ...     context={"cliente_id": "12345"}
        ... )
    """
    
    def __init__(self, message: str, rule_name: str = None, context: dict = None):
        self.rule_name = rule_name
        self.context = context or {}
        
        super().__init__(message)
        
    def __str__(self):
        base_message = super().__str__()
        if self.rule_name:
            return f"[{self.rule_name}] {base_message}"
        return base_message
