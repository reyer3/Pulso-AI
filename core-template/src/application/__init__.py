# ⚙️ Application Layer - Pulso-AI
# Casos de uso y orquestación de la lógica de negocio

"""
Application Layer - Arquitectura Hexagonal

Esta capa coordina la ejecución de casos de uso y orquesta:
- Llamadas al domain layer
- Uso de repositories (a través de interfaces)
- Manejo de transacciones
- Coordinación de servicios

Contiene:
- use_cases/: Casos de uso específicos del negocio
- services/: Servicios de aplicación para coordinación
- dto/: Data Transfer Objects para comunicación entre capas
- interfaces/: Definición de contratos con infrastructure

Principio: Esta capa no debe contener lógica de negocio,
solo orquestación y coordinación.
"""
