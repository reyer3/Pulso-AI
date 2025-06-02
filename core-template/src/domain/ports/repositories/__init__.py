"""Repository interfaces for data persistence.

Repository ports define contracts for data access without
specifying HOW data is stored or retrieved. This enables
swapping between BigQuery, PostgreSQL, MySQL seamlessly.

Key Principles:
    - Client-agnostic: Work with any data source
    - Async by default: Support high-performance I/O
    - Business-focused: Methods reflect domain needs
    - Type-safe: Full type hints for better development experience

Example Multi-Client Usage:
    # Same interface, different implementations
    movistar_repo = BigQueryClienteRepository()  # BigQuery
    claro_repo = PostgreSQLClienteRepository()   # PostgreSQL
    tigo_repo = MySQLClienteRepository()         # MySQL
    
    # All implement same ClienteRepository interface
    for repo in [movistar_repo, claro_repo, tigo_repo]:
        clientes = await repo.find_clientes_en_mora(30)
"""

from .base_repository import BaseRepository
from .cliente_repository import ClienteRepository
from .gestion_repository import GestionRepository

__all__ = [
    "BaseRepository",
    "ClienteRepository",
    "GestionRepository"
]
