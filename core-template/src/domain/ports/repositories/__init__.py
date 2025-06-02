"""Repository interfaces for domain entities.

This module defines the contracts (ports) for data persistence
operations. Each repository interface focuses on a specific
entity or aggregate root.

Key principles:
- Interfaces are defined by domain needs, not infrastructure capabilities
- All methods are async for scalability
- Type hints are comprehensive for clarity
- Methods are granular and focused

Example:
    >>> from domain.ports.repositories import ClienteRepository
    >>> 
    >>> class MyUseCase:
    ...     def __init__(self, cliente_repo: ClienteRepository):
    ...         self.cliente_repo = cliente_repo
    ...     
    ...     async def execute(self, documento: str):
    ...         cliente = await self.cliente_repo.find_by_documento(documento)
    ...         return cliente
"""

from .base_repository import BaseRepository
from .cliente_repository import ClienteRepository
from .gestion_repository import GestionRepository

__all__ = [
    "BaseRepository",
    "ClienteRepository",
    "GestionRepository"
]
