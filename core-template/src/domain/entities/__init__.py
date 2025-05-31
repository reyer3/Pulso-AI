"""Domain entities package.

This package contains the core business entities that represent
the fundamental concepts in the debt collection domain.

Entities are pure Python objects with business behavior,
following Domain-Driven Design principles.
"""

from .cliente import Cliente
from .gestion import Gestion
from .metrica import Metrica

__all__ = ["Cliente", "Gestion", "Metrica"]
