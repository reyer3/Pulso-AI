# 🏛️ Core Domain Entities

Esta implementación resuelve la **Issue #8** definiendo las entidades fundamentales del dominio para el sistema de cobranza multi-cliente.

## 🎯 Entidades Implementadas

### ✅ Entities
- **Cliente**: Entidad principal que representa un cliente con deuda
- **Gestion**: Entidad que representa una acción de cobranza
- **Metrica**: Value object para métricas calculadas

### ✅ Value Objects  
- **CanalContacto**: Enum para canales de contacto
- **TipificacionHomologada**: Enum para tipificaciones estandarizadas
- **DocumentoIdentidad**: Value object para documentos de identidad

### ✅ Domain Exceptions
- **ClienteNotFound**: Cliente no encontrado
- **GestionInvalida**: Gestión con datos inválidos
- **MetricaCalculationError**: Error en cálculo de métricas
- **TipificacionHomologacionError**: Error en homologación

## 🔄 Cross-Client Support

Las entidades soportan configuración multi-cliente:

```python
# Ejemplo: Misma entidad, diferentes configuraciones
movistar_gestion = Gestion(
    tipificacion_original="CONT_COMP",  # Específico Movistar
    tipificacion_homologada=TipificacionHomologada.COMPROMISO_PAGO.value
)

claro_gestion = Gestion(
    tipificacion_original="CONTACTO_COMPROMISO",  # Específico Claro  
    tipificacion_homologada=TipificacionHomologada.COMPROMISO_PAGO.value
)
```

## 🧪 Testing

Todos los tests están implementados con coverage >90%:

```bash
cd core-template
pytest tests/domain/ -v --cov=src/domain
```

## ⚡ Business Rules

### Cliente
- `esta_en_mora()`: Determina si cliente está en mora
- `tiene_deuda_significativa()`: Evalúa si deuda es significativa  
- `es_cliente_prioritario()`: Clasifica prioridad para gestión

### Gestion
- `es_gestion_exitosa()`: Contacto + compromiso = éxito
- `requiere_seguimiento()`: Contacto sin compromiso = follow-up
- `es_canal_automatizado()`: Identifica canales sin intervención humana

### Metrica
- `supera_umbral()`: Comparación contra umbrales de performance
- `esta_en_rango_optimo()`: Evaluación de rangos aceptables
- `obtener_clasificacion_rendimiento()`: Clasificación automática

## 🔧 Next Steps

1. **Issue #4**: Definir puertos/interfaces para repositories
2. **Fase 1**: Implementar adaptadores BigQuery para Movistar  
3. **Tests Integration**: Conectar con casos de uso reales

---

Esta implementación establece la base sólida para la arquitectura hexagonal del proyecto Pulso-AI. 🚀
