"""Domain value objects package.

This package contains value objects and enums that represent
concepts without identity in the domain model.

Value objects are immutable and equality is based on their values,
not identity.
"""

from .enums import CanalContacto, TipificacionHomologada
from .identificadores import DocumentoIdentidad

__all__ = [
    "CanalContacto",
    "TipificacionHomologada", 
    "DocumentoIdentidad"
]
