# 🚀 Pulso-AI Core Template
# Template base para todos los clientes multi-tenant

"""
Pulso-AI Core Template

Este paquete contiene la lógica base reutilizable para todos los clientes.
Sigue arquitectura hexagonal con separación clara de responsabilidades:

- domain/: Lógica de negocio pura (entities, value objects, business rules)
- application/: Casos de uso y orquestación
- infrastructure/: Adaptadores para bases de datos y servicios externos
- api/: Interfaces HTTP/GraphQL

Principios:
- Domain-driven design
- Dependency inversion
- Configuration over code
- Multi-tenant by design
"""

__version__ = "0.1.0"
__author__ = "Pulso-AI Contributors"
__email__ = "contributors@pulso-ai.dev"

# Export principales
from .domain.entities import Cliente, Gestion, Metrica
from .domain.value_objects import FilterState, DimensionConfig
from .application.use_cases import (
    IntegrateClientDataUseCase,
    GenerateDashboardUseCase,
    CrossFilterUseCase,
)

__all__ = [
    "Cliente",
    "Gestion", 
    "Metrica",
    "FilterState",
    "DimensionConfig",
    "IntegrateClientDataUseCase",
    "GenerateDashboardUseCase", 
    "CrossFilterUseCase",
]
