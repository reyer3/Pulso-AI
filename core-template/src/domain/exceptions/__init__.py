"""Domain exceptions package.

Contains all domain-specific exceptions that represent business rule violations
or domain invariant failures. These exceptions are part of the domain language.

Exceptions:
    ClienteNotFound: Cliente does not exist
    GestionInvalida: Invalid gestion data or business rule violation
    MetricaCalculationError: Error calculating metric
    DomainValidationError: Generic domain validation failure
"""

from .domain_exceptions import (
    ClienteNotFound,
    GestionInvalida,
    MetricaCalculationError,
    DomainValidationError,
    TipificacionHomologacionError
)

__all__ = [
    "ClienteNotFound",
    "GestionInvalida", 
    "MetricaCalculationError",
    "DomainValidationError",
    "TipificacionHomologacionError"
]
