# 🌐 API Layer - Pulso-AI
# Interfaces HTTP y GraphQL para comunicación externa

"""
API Layer - Arquitectura Hexagonal

Esta capa expone la funcionalidad del sistema a través de:
- REST endpoints (FastAPI)
- GraphQL endpoints (Strawberry)
- WebSocket connections
- Middleware y autenticación

Contiene:
- graphql/: Schema y resolvers de GraphQL
  - schemas/: Definiciones de tipos GraphQL
  - resolvers/: Lógica de resolución de queries/mutations
  - middleware/: Middleware específico de GraphQL
- rest/: Endpoints REST para operaciones específicas
- websocket/: Conexiones en tiempo real
- auth/: Middleware de autenticación y autorización
- middleware/: Middleware global (CORS, logging, etc.)

Principio: Esta capa traduce requests externos a llamadas de application layer
y formatea las respuestas apropiadamente.
"""
