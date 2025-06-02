"""Domain exceptions package.

This package contains domain-specific exceptions that represent
business rule violations and domain-level errors.

These exceptions should be used when domain invariants are violated
or when business operations cannot be completed.
"""

from .domain_exceptions import (
    DomainException,
    ClienteNotFound,
    GestionInvalida,
    MetricaInvalida,
    HomologacionError,
    ReglaNegocioViolada
)

__all__ = [
    "DomainException",
    "ClienteNotFound",
    "GestionInvalida", 
    "MetricaInvalida",
    "HomologacionError",
    "ReglaNegocioViolada"
]
