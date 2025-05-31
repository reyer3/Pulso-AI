"""Domain entities package.

Contains the core business entities that represent the fundamental concepts
of the debt collection/cobranza domain. These entities are pure Python classes
with zero external dependencies, containing business logic and rules.

Entities:
    Cliente: Core entity representing a customer with debt
    Gestion: Entity representing a collection management action
    Metrica: Value object for calculated metrics
"""

from .cliente import Cliente
from .gestion import Gestion
from .metrica import Metrica

__all__ = ["Cliente", "Gestion", "Metrica"]
