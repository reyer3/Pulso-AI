"""Tests for domain enums."""

import pytest

from src.domain.value_objects.enums import (
    CanalContacto,
    TipificacionHomologada,
    EstadoCliente,
    PrioridadCobranza
)


class TestCanalContacto:
    """Test suite for CanalContacto enum."""
    
    def test_canal_contacto_values(self):
        """Test all CanalContacto enum values exist."""
        expected_values = [
            "CALL", "VOICEBOT", "EMAIL", "SMS", 
            "WHATSAPP", "VISITA_DOMICILIO", "CARTA", "CALL_CENTER"
        ]
        
        actual_values = [canal.value for canal in CanalContacto]
        
        for expected in expected_values:
            assert expected in actual_values
    
    def test_es_canal_directo_true(self):
        """Test es_canal_directo returns True for direct channels."""
        direct_channels = [
            CanalContacto.CALL,
            CanalContacto.WHATSAPP,
            CanalContacto.VISITA_DOMICILIO
        ]
        
        for canal in direct_channels:
            assert canal.es_canal_directo() is True
    
    def test_es_canal_directo_false(self):
        """Test es_canal_directo returns False for indirect channels."""
        indirect_channels = [
            CanalContacto.EMAIL,
            CanalContacto.SMS,
            CanalContacto.VOICEBOT,
            CanalContacto.CARTA,
            CanalContacto.CALL_CENTER
        ]
        
        for canal in indirect_channels:
            assert canal.es_canal_directo() is False
    
    def test_es_canal_digital_true(self):
        """Test es_canal_digital returns True for digital channels."""
        digital_channels = [
            CanalContacto.EMAIL,
            CanalContacto.SMS,
            CanalContacto.WHATSAPP,
            CanalContacto.VOICEBOT
        ]
        
        for canal in digital_channels:
            assert canal.es_canal_digital() is True
    
    def test_es_canal_digital_false(self):
        """Test es_canal_digital returns False for non-digital channels."""
        non_digital_channels = [
            CanalContacto.CALL,
            CanalContacto.VISITA_DOMICILIO,
            CanalContacto.CARTA,
            CanalContacto.CALL_CENTER
        ]
        
        for canal in non_digital_channels:
            assert canal.es_canal_digital() is False
    
    def test_es_canal_automatizado_true(self):
        """Test es_canal_automatizado returns True for automated channels."""
        automated_channels = [
            CanalContacto.VOICEBOT,
            CanalContacto.SMS
        ]
        
        for canal in automated_channels:
            assert canal.es_canal_automatizado() is True
    
    def test_es_canal_automatizado_false(self):
        """Test es_canal_automatizado returns False for non-automated channels."""
        non_automated = [
            CanalContacto.CALL,
            CanalContacto.EMAIL,
            CanalContacto.WHATSAPP,
            CanalContacto.VISITA_DOMICILIO,
            CanalContacto.CARTA,
            CanalContacto.CALL_CENTER
        ]
        
        for canal in non_automated:
            assert canal.es_canal_automatizado() is False
    
    def test_requiere_agente_humano_true(self):
        """Test requiere_agente_humano returns True when needed."""
        human_required = [
            CanalContacto.CALL,
            CanalContacto.WHATSAPP,
            CanalContacto.VISITA_DOMICILIO,
            CanalContacto.CALL_CENTER
        ]
        
        for canal in human_required:
            assert canal.requiere_agente_humano() is True
    
    def test_requiere_agente_humano_false(self):
        """Test requiere_agente_humano returns False when not needed."""
        no_human_required = [
            CanalContacto.VOICEBOT,
            CanalContacto.EMAIL,
            CanalContacto.SMS,
            CanalContacto.CARTA
        ]
        
        for canal in no_human_required:
            assert canal.requiere_agente_humano() is False
    
    def test_canales_de_alta_conversion(self):
        """Test canales_de_alta_conversion class method."""
        high_conversion = CanalContacto.canales_de_alta_conversion()
        
        expected = [
            CanalContacto.CALL,
            CanalContacto.WHATSAPP,
            CanalContacto.VISITA_DOMICILIO
        ]
        
        assert high_conversion == expected
    
    def test_canales_de_bajo_costo(self):
        """Test canales_de_bajo_costo class method."""
        low_cost = CanalContacto.canales_de_bajo_costo()
        
        expected = [
            CanalContacto.EMAIL,
            CanalContacto.SMS,
            CanalContacto.VOICEBOT
        ]
        
        assert low_cost == expected


class TestTipificacionHomologada:
    """Test suite for TipificacionHomologada enum."""
    
    def test_tipificacion_values_exist(self):
        """Test all expected tipification values exist."""
        expected_values = [
            "CONTACTO_EFECTIVO", "COMPROMISO_PAGO", "PAGO_INMEDIATO",
            "ACUERDO_PAGO", "NO_CONTACTO", "NUMERO_ERRADO",
            "TELEFONO_APAGADO", "BUZON_VOZ", "NO_INTERESADO",
            "SIN_CAPACIDAD_PAGO", "SOLICITA_FACILIDADES",
            "DISPUTA_DEUDA", "FALLECIDO", "CAMBIO_DATOS", "RECLAMO_CLIENTE"
        ]
        
        actual_values = [tip.value for tip in TipificacionHomologada]
        
        for expected in expected_values:
            assert expected in actual_values
    
    def test_es_resultado_positivo_true(self):
        """Test es_resultado_positivo returns True for positive outcomes."""
        positive_outcomes = [
            TipificacionHomologada.CONTACTO_EFECTIVO,
            TipificacionHomologada.COMPROMISO_PAGO,
            TipificacionHomologada.PAGO_INMEDIATO,
            TipificacionHomologada.ACUERDO_PAGO,
            TipificacionHomologada.SOLICITA_FACILIDADES
        ]
        
        for tip in positive_outcomes:
            assert tip.es_resultado_positivo() is True
    
    def test_es_resultado_positivo_false(self):
        """Test es_resultado_positivo returns False for negative outcomes."""
        negative_outcomes = [
            TipificacionHomologada.NO_CONTACTO,
            TipificacionHomologada.NUMERO_ERRADO,
            TipificacionHomologada.NO_INTERESADO,
            TipificacionHomologada.DISPUTA_DEUDA
        ]
        
        for tip in negative_outcomes:
            assert tip.es_resultado_positivo() is False
    
    def test_indica_contacto_efectivo_true(self):
        """Test indica_contacto_efectivo returns True when contact was made."""
        contact_made = [
            TipificacionHomologada.CONTACTO_EFECTIVO,
            TipificacionHomologada.COMPROMISO_PAGO,
            TipificacionHomologada.NO_INTERESADO,
            TipificacionHomologada.DISPUTA_DEUDA
        ]
        
        for tip in contact_made:
            assert tip.indica_contacto_efectivo() is True
    
    def test_indica_contacto_efectivo_false(self):
        """Test indica_contacto_efectivo returns False when no contact."""
        no_contact = [
            TipificacionHomologada.NO_CONTACTO,
            TipificacionHomologada.NUMERO_ERRADO,
            TipificacionHomologada.TELEFONO_APAGADO,
            TipificacionHomologada.BUZON_VOZ
        ]
        
        for tip in no_contact:
            assert tip.indica_contacto_efectivo() is False
    
    def test_requiere_seguimiento_true(self):
        """Test requiere_seguimiento returns True when follow-up needed."""
        needs_followup = [
            TipificacionHomologada.COMPROMISO_PAGO,
            TipificacionHomologada.ACUERDO_PAGO,
            TipificacionHomologada.SOLICITA_FACILIDADES,
            TipificacionHomologada.CAMBIO_DATOS,
            TipificacionHomologada.RECLAMO_CLIENTE
        ]
        
        for tip in needs_followup:
            assert tip.requiere_seguimiento() is True
    
    def test_requiere_seguimiento_false(self):
        """Test requiere_seguimiento returns False when no follow-up needed."""
        no_followup = [
            TipificacionHomologada.PAGO_INMEDIATO,
            TipificacionHomologada.NO_CONTACTO,
            TipificacionHomologada.NO_INTERESADO
        ]
        
        for tip in no_followup:
            assert tip.requiere_seguimiento() is False
    
    def test_es_caso_especial_true(self):
        """Test es_caso_especial returns True for special cases."""
        special_cases = [
            TipificacionHomologada.DISPUTA_DEUDA,
            TipificacionHomologada.FALLECIDO,
            TipificacionHomologada.RECLAMO_CLIENTE
        ]
        
        for tip in special_cases:
            assert tip.es_caso_especial() is True
    
    def test_es_caso_especial_false(self):
        """Test es_caso_especial returns False for normal cases."""
        normal_cases = [
            TipificacionHomologada.CONTACTO_EFECTIVO,
            TipificacionHomologada.NO_CONTACTO,
            TipificacionHomologada.COMPROMISO_PAGO
        ]
        
        for tip in normal_cases:
            assert tip.es_caso_especial() is False
    
    def test_tipificaciones_de_exito_class_method(self):
        """Test tipificaciones_de_exito class method."""
        successful = TipificacionHomologada.tipificaciones_de_exito()
        
        expected = [
            TipificacionHomologada.COMPROMISO_PAGO,
            TipificacionHomologada.PAGO_INMEDIATO,
            TipificacionHomologada.ACUERDO_PAGO
        ]
        
        assert successful == expected
    
    def test_tipificaciones_de_contacto_class_method(self):
        """Test tipificaciones_de_contacto class method."""
        contact_tips = TipificacionHomologada.tipificaciones_de_contacto()
        
        # Should include all tips that indicate contact was made
        no_contact_tips = [
            TipificacionHomologada.NO_CONTACTO,
            TipificacionHomologada.NUMERO_ERRADO,
            TipificacionHomologada.TELEFONO_APAGADO,
            TipificacionHomologada.BUZON_VOZ
        ]
        
        for tip in contact_tips:
            assert tip not in no_contact_tips
            assert tip.indica_contacto_efectivo() is True


class TestEstadoCliente:
    """Test suite for EstadoCliente enum."""
    
    def test_estado_cliente_values(self):
        """Test all EstadoCliente enum values exist."""
        expected_values = [
            "ACTIVO", "INACTIVO", "EXCLUIDO", 
            "JURIDICO", "PAGADO", "CASTIGADO"
        ]
        
        actual_values = [estado.value for estado in EstadoCliente]
        
        for expected in expected_values:
            assert expected in actual_values


class TestPrioridadCobranza:
    """Test suite for PrioridadCobranza enum."""
    
    def test_prioridad_cobranza_values(self):
        """Test all PrioridadCobranza enum values exist."""
        expected_values = ["ALTA", "MEDIA", "BAJA", "CRITICA"]
        
        actual_values = [prioridad.value for prioridad in PrioridadCobranza]
        
        for expected in expected_values:
            assert expected in actual_values
    
    def test_nivel_numerico(self):
        """Test nivel_numerico method returns correct values."""
        assert PrioridadCobranza.CRITICA.nivel_numerico() == 4
        assert PrioridadCobranza.ALTA.nivel_numerico() == 3
        assert PrioridadCobranza.MEDIA.nivel_numerico() == 2
        assert PrioridadCobranza.BAJA.nivel_numerico() == 1
    
    def test_nivel_numerico_ordering(self):
        """Test that numeric levels maintain proper ordering."""
        assert (
            PrioridadCobranza.CRITICA.nivel_numerico() >
            PrioridadCobranza.ALTA.nivel_numerico() >
            PrioridadCobranza.MEDIA.nivel_numerico() >
            PrioridadCobranza.BAJA.nivel_numerico()
        )


class TestEnumsIntegration:
    """Test integration between different enums."""
    
    def test_canal_y_tipificacion_consistency(self):
        """Test that high-conversion channels align with positive tipifications."""
        high_conversion_channels = CanalContacto.canales_de_alta_conversion()
        successful_tipifications = TipificacionHomologada.tipificaciones_de_exito()
        
        # High conversion channels should be those that require human agent
        for canal in high_conversion_channels:
            assert canal.requiere_agente_humano() is True
        
        # Successful tipifications should all be positive outcomes
        for tip in successful_tipifications:
            assert tip.es_resultado_positivo() is True
    
    def test_business_logic_consistency(self):
        """Test business logic consistency across enums."""
        # Automated channels should be low cost
        low_cost = CanalContacto.canales_de_bajo_costo()
        
        for canal in low_cost:
            # Most low cost channels should be automated or not require humans
            assert (
                canal.es_canal_automatizado() or 
                not canal.requiere_agente_humano()
            )
