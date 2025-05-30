# 🏗️ Domain Layer - Pulso-AI
# Lógica de negocio pura sin dependencias externas

"""
Domain Layer - Arquitectura Hexagonal

Esta capa contiene la lógica de negocio pura y no debe depender de:
- Frameworks web
- Bases de datos
- APIs externas
- Cualquier infraestructura

Contiene:
- entities/: Entidades de negocio (Cliente, Gestion, Metrica)
- value_objects/: Objetos de valor inmutables
- services/: Servicios de dominio para lógica compleja
- repositories/: Interfaces (puertos) para persistencia
- events/: Eventos de dominio para comunicación asíncrona
"""
