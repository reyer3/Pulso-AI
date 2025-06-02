"""Tests for Cliente domain entity."""

import pytest
from datetime import datetime

from src.domain.entities.cliente import Cliente


class TestCliente:
    """Test suite for Cliente entity."""
    
    def test_cliente_creation_success(self):
        """Test successful cliente creation."""
        cliente = Cliente(
            documento="12345678",
            nombre="Juan Pérez",
            saldo_actual=1500.50,
            dias_mora=45,
            telefono="987654321",
            email="juan@email.com"
        )
        
        assert cliente.documento == "12345678"
        assert cliente.nombre == "Juan Pérez"
        assert cliente.saldo_actual == 1500.50
        assert cliente.dias_mora == 45
        assert cliente.telefono == "987654321"
        assert cliente.email == "juan@email.com"
    
    def test_cliente_creation_minimal(self):
        """Test cliente creation with minimal required fields."""
        cliente = Cliente(
            documento="12345678",
            nombre="Juan Pérez",
            saldo_actual=1500.50,
            dias_mora=45
        )
        
        assert cliente.telefono is None
        assert cliente.email is None
        assert cliente.ultima_actualizacion is None
    
    def test_cliente_validation_documento_empty(self):
        """Test validation fails for empty documento."""
        with pytest.raises(ValueError, match="Documento no puede estar vacío"):
            Cliente(
                documento="",
                nombre="Juan Pérez",
                saldo_actual=1500.50,
                dias_mora=45
            )
    
    def test_cliente_validation_documento_whitespace(self):
        """Test validation fails for whitespace-only documento."""
        with pytest.raises(ValueError, match="Documento no puede estar vacío"):
            Cliente(
                documento="   ",
                nombre="Juan Pérez",
                saldo_actual=1500.50,
                dias_mora=45
            )
    
    def test_cliente_validation_nombre_empty(self):
        """Test validation fails for empty nombre."""
        with pytest.raises(ValueError, match="Nombre no puede estar vacío"):
            Cliente(
                documento="12345678",
                nombre="",
                saldo_actual=1500.50,
                dias_mora=45
            )
    
    def test_cliente_validation_saldo_negativo(self):
        """Test validation fails for negative saldo."""
        with pytest.raises(ValueError, match="Saldo actual no puede ser negativo"):
            Cliente(
                documento="12345678",
                nombre="Juan Pérez",
                saldo_actual=-100.0,
                dias_mora=45
            )
    
    def test_cliente_validation_dias_mora_negativos(self):
        """Test validation fails for negative dias_mora."""
        with pytest.raises(ValueError, match="Días de mora no pueden ser negativos"):
            Cliente(
                documento="12345678",
                nombre="Juan Pérez",
                saldo_actual=1500.50,
                dias_mora=-10
            )
    
    def test_esta_en_mora_default_threshold(self):
        """Test esta_en_mora with default threshold (30 days)."""
        cliente_en_mora = Cliente("123", "Juan", 500.0, 45)
        cliente_sin_mora = Cliente("123", "Pedro", 500.0, 15)
        cliente_limite = Cliente("123", "Ana", 500.0, 30)
        
        assert cliente_en_mora.esta_en_mora() is True
        assert cliente_sin_mora.esta_en_mora() is False
        assert cliente_limite.esta_en_mora() is True  # >= 30
    
    def test_esta_en_mora_custom_threshold(self):
        """Test esta_en_mora with custom threshold."""
        cliente = Cliente("123", "Juan", 500.0, 45)
        
        assert cliente.esta_en_mora(30) is True
        assert cliente.esta_en_mora(60) is False
        assert cliente.esta_en_mora(45) is True  # Exactly equal
    
    def test_tiene_deuda_significativa_default(self):
        """Test tiene_deuda_significativa with default threshold."""
        cliente_deuda_alta = Cliente("123", "Juan", 500.0, 30)
        cliente_deuda_baja = Cliente("123", "Pedro", 50.0, 30)
        cliente_limite = Cliente("123", "Ana", 100.0, 30)
        
        assert cliente_deuda_alta.tiene_deuda_significativa() is True
        assert cliente_deuda_baja.tiene_deuda_significativa() is False
        assert cliente_limite.tiene_deuda_significativa() is True  # >= 100
    
    def test_tiene_deuda_significativa_custom(self):
        """Test tiene_deuda_significativa with custom threshold."""
        cliente = Cliente("123", "Juan", 500.0, 30)
        
        assert cliente.tiene_deuda_significativa(100.0) is True
        assert cliente.tiene_deuda_significativa(1000.0) is False
        assert cliente.tiene_deuda_significativa(500.0) is True  # Exactly equal
    
    def test_requiere_atencion_urgente_true(self):
        """Test requiere_atencion_urgente returns True when both conditions met."""
        cliente = Cliente("123", "Juan", 1500.0, 100)
        
        assert cliente.requiere_atencion_urgente(90, 1000.0) is True
    
    def test_requiere_atencion_urgente_false_dias(self):
        """Test requiere_atencion_urgente returns False when days not critical."""
        cliente = Cliente("123", "Juan", 1500.0, 80)  # Less than 90 days
        
        assert cliente.requiere_atencion_urgente(90, 1000.0) is False
    
    def test_requiere_atencion_urgente_false_monto(self):
        """Test requiere_atencion_urgente returns False when amount not critical."""
        cliente = Cliente("123", "Juan", 800.0, 100)  # Less than 1000
        
        assert cliente.requiere_atencion_urgente(90, 1000.0) is False
    
    def test_requiere_atencion_urgente_false_both(self):
        """Test requiere_atencion_urgente returns False when neither condition met."""
        cliente = Cliente("123", "Juan", 800.0, 80)
        
        assert cliente.requiere_atencion_urgente(90, 1000.0) is False
    
    def test_calcular_prioridad_cobranza_alta(self):
        """Test calcular_prioridad_cobranza returns ALTA."""
        cliente = Cliente("123", "Juan", 2000.0, 120)
        
        assert cliente.calcular_prioridad_cobranza() == "ALTA"
    
    def test_calcular_prioridad_cobranza_media(self):
        """Test calcular_prioridad_cobranza returns MEDIA."""
        cliente = Cliente("123", "Juan", 800.0, 45)  # En mora + deuda significativa
        
        assert cliente.calcular_prioridad_cobranza() == "MEDIA"
    
    def test_calcular_prioridad_cobranza_baja(self):
        """Test calcular_prioridad_cobranza returns BAJA."""
        cliente = Cliente("123", "Juan", 200.0, 15)  # No urgente, no mora crítica
        
        assert cliente.calcular_prioridad_cobranza() == "BAJA"
    
    def test_es_contactable_con_telefono(self):
        """Test es_contactable returns True when has phone."""
        cliente = Cliente("123", "Juan", 500.0, 30, telefono="987654321")
        
        assert cliente.es_contactable() is True
    
    def test_es_contactable_con_email(self):
        """Test es_contactable returns True when has email."""
        cliente = Cliente("123", "Juan", 500.0, 30, email="juan@email.com")
        
        assert cliente.es_contactable() is True
    
    def test_es_contactable_con_ambos(self):
        """Test es_contactable returns True when has both."""
        cliente = Cliente(
            "123", "Juan", 500.0, 30, 
            telefono="987654321", 
            email="juan@email.com"
        )
        
        assert cliente.es_contactable() is True
    
    def test_es_contactable_sin_contacto(self):
        """Test es_contactable returns False when has no contact info."""
        cliente = Cliente("123", "Juan", 500.0, 30)
        
        assert cliente.es_contactable() is False
    
    def test_str_representation(self):
        """Test string representation of cliente."""
        cliente = Cliente("12345678", "Juan Pérez", 1500.50, 45)
        
        expected = "Cliente(doc=12345678, nombre=Juan Pérez, deuda=1500.5)"
        assert str(cliente) == expected
    
    def test_equality_same_documento(self):
        """Test equality based on documento (business key)."""
        cliente1 = Cliente("12345678", "Juan Pérez", 1500.50, 45)
        cliente2 = Cliente("12345678", "Juan Pérez García", 2000.0, 60)
        
        assert cliente1 == cliente2
    
    def test_equality_different_documento(self):
        """Test inequality when documento is different."""
        cliente1 = Cliente("12345678", "Juan Pérez", 1500.50, 45)
        cliente2 = Cliente("87654321", "Juan Pérez", 1500.50, 45)
        
        assert cliente1 != cliente2
    
    def test_equality_different_type(self):
        """Test inequality when comparing with different type."""
        cliente = Cliente("12345678", "Juan Pérez", 1500.50, 45)
        
        assert cliente != "not a cliente"
        assert cliente != 123
        assert cliente != None
    
    def test_hash_consistency(self):
        """Test hash consistency for same documento."""
        cliente1 = Cliente("12345678", "Juan Pérez", 1500.50, 45)
        cliente2 = Cliente("12345678", "Juan Pérez García", 2000.0, 60)
        
        assert hash(cliente1) == hash(cliente2)
    
    def test_hash_different_documento(self):
        """Test different hash for different documento."""
        cliente1 = Cliente("12345678", "Juan Pérez", 1500.50, 45)
        cliente2 = Cliente("87654321", "Juan Pérez", 1500.50, 45)
        
        assert hash(cliente1) != hash(cliente2)
    
    def test_zero_values(self):
        """Test cliente with zero values (edge case)."""
        cliente = Cliente("123", "Juan", 0.0, 0)
        
        assert cliente.saldo_actual == 0.0
        assert cliente.dias_mora == 0
        assert cliente.esta_en_mora(1) is False
        assert cliente.tiene_deuda_significativa(0.01) is False
        assert cliente.calcular_prioridad_cobranza() == "BAJA"


class TestClienteBusinessRules:
    """Test suite for Cliente business rules integration."""
    
    def test_scenario_cliente_critico(self):
        """Test complete scenario: critical customer."""
        cliente = Cliente("12345678", "Juan Pérez", 5000.0, 150)
        
        # Should be critical across all metrics
        assert cliente.esta_en_mora(30) is True
        assert cliente.tiene_deuda_significativa(1000.0) is True
        assert cliente.requiere_atencion_urgente(90, 1500.0) is True
        assert cliente.calcular_prioridad_cobranza() == "ALTA"
    
    def test_scenario_cliente_nuevo(self):
        """Test complete scenario: new customer, low risk."""
        cliente = Cliente("12345678", "Ana García", 250.0, 10)
        
        # Should be low priority
        assert cliente.esta_en_mora(30) is False
        assert cliente.tiene_deuda_significativa(500.0) is False
        assert cliente.requiere_atencion_urgente() is False
        assert cliente.calcular_prioridad_cobranza() == "BAJA"
    
    def test_scenario_cliente_intermedio(self):
        """Test complete scenario: medium priority customer."""
        cliente = Cliente("12345678", "Carlos López", 800.0, 50)
        
        # Should be medium priority
        assert cliente.esta_en_mora(30) is True
        assert cliente.tiene_deuda_significativa(500.0) is True
        assert cliente.requiere_atencion_urgente(90, 1500.0) is False
        assert cliente.calcular_prioridad_cobranza() == "MEDIA"
