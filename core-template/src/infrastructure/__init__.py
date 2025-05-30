# 🔌 Infrastructure Layer - Pulso-AI
# Adaptadores y conectores con sistemas externos

"""
Infrastructure Layer - Arquitectura Hexagonal

Esta capa implementa los adaptadores para sistemas externos:
- Bases de datos (PostgreSQL, BigQuery, MySQL)
- Servicios de cache (Redis)
- APIs externas
- Sistemas de archivos
- Message queues

Contiene:
- adapters/: Implementaciones de interfaces del domain
  - database/: Adaptadores para diferentes bases de datos
  - cache/: Adaptadores para sistemas de cache
  - external_apis/: Conectores con APIs externas
- repositories/: Implementaciones concretas de repositories
- config/: Configuración de infraestructura
- migrations/: Scripts de migración de base de datos

Principio: Esta capa implementa las interfaces definidas en domain/application
y maneja toda la comunicación con sistemas externos.
"""
