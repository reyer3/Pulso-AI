"""Domain value objects package.

Contains immutable value objects that represent concepts without identity.
Includes enums, identifiers, and other value types used across the domain.

Value Objects:
    CanalContacto: Enum for contact channels
    TipificacionHomologada: Enum for standardized tipifications
    DocumentoIdentidad: Value object for identity documents
"""

from .enums import CanalContacto, TipificacionHomologada
from .identificadores import DocumentoIdentidad

__all__ = [
    "CanalContacto",
    "TipificacionHomologada", 
    "DocumentoIdentidad"
]
