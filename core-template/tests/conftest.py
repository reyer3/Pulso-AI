"""Pytest configuration and shared fixtures."""

import pytest
from datetime import datetime
from typing import Dict, Any

from src.domain.entities.cliente import Cliente
from src.domain.entities.gestion import Gestion
from src.domain.value_objects.enums import CanalContacto, TipificacionHomologada


@pytest.fixture
def cliente_basico() -> Cliente:
    """Basic cliente fixture for testing."""
    return Cliente(
        documento="12345678",
        nombre="Juan Pérez",
        saldo_actual=1500.50,
        dias_mora=45,
        telefono="987654321",
        email="juan@email.com"
    )


@pytest.fixture
def cliente_critico() -> Cliente:
    """Critical priority cliente fixture."""
    return Cliente(
        documento="87654321",
        nombre="María García",
        saldo_actual=5000.0,
        dias_mora=150
    )


@pytest.fixture
def cliente_bajo_riesgo() -> Cliente:
    """Low risk cliente fixture."""
    return Cliente(
        documento="11111111",
        nombre="Pedro López",
        saldo_actual=200.0,
        dias_mora=5
    )


@pytest.fixture
def gestion_exitosa() -> Gestion:
    """Successful gestion fixture."""
    return Gestion(
        id="gest-001",
        documento_cliente="12345678",
        fecha=datetime(2025, 6, 1, 10, 30),
        canal=CanalContacto.CALL,
        ejecutivo="Ana García",
        tipificacion_original="CONT_COMP",
        tipificacion_homologada=TipificacionHomologada.COMPROMISO_PAGO,
        es_contacto=True,
        es_compromiso=True
    )


@pytest.fixture
def gestion_sin_contacto() -> Gestion:
    """No contact gestion fixture."""
    return Gestion(
        id="gest-002",
        documento_cliente="87654321",
        fecha=datetime(2025, 6, 1, 14, 15),
        canal=CanalContacto.CALL,
        ejecutivo="Carlos Ruiz",
        tipificacion_original="NO_RESP",
        tipificacion_homologada=TipificacionHomologada.NO_CONTACTO,
        es_contacto=False,
        es_compromiso=False
    )


@pytest.fixture
def sample_client_config() -> Dict[str, Any]:
    """Sample client configuration for testing homologation."""
    return {
        "client_id": "movistar-peru",
        "name": "Movistar Perú",
        "field_mappings": {
            "ejecutivo_field": "ejecutivo",
            "documento_field": "documento",
            "nombre_field": "nombre_cliente"
        },
        "tipificacion_mappings": {
            "CONT_COMP": TipificacionHomologada.COMPROMISO_PAGO.value,
            "NO_RESP": TipificacionHomologada.NO_CONTACTO.value,
            "PAGO_HOY": TipificacionHomologada.PAGO_INMEDIATO.value
        }
    }
