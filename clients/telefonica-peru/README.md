# 📞 Telefónica del Perú - Configuración Cliente

**Cliente**: Telefónica del Perú (Movistar)  
**Región**: Perú  
**Modelo de negocio**: Gestión de cobranza  
**Estado**: ✅ **FUENTES REALES IDENTIFICADAS** (Corrección crítica aplicada)

## 🔍 **CORRECCIÓN CRÍTICA REALIZADA**

❌ **ANTES** (Configuración especulativa):
```
Fuente: dash_P3fV4dWNeMkN5RJMhV8e_vw_operativo (NO EXISTE)
```

✅ **DESPUÉS** (Fuentes reales identificadas):
```
📊 8 TABLAS REALES IDENTIFICADAS EN BIGQUERY:
├── 6 Tablas Batch (maestros + transaccionales)
└── 2 Tablas Operativas (gestiones CALL + VOICEBOT)
```

## 📊 **FUENTES DE DATOS REALES**

### **🗂️ Tablas Batch (Maestros + Transaccionales)**
```
Project: mibot-222814
Dataset: BI_USA

├── batch_P3fV4dWNeMkN5RJMhV8e_asignacion     # Universo de clientes
├── batch_P3fV4dWNeMkN5RJMhV8e_master_luna    # Maestro clientes
├── batch_P3fV4dWNeMkN5RJMhV8e_master_contacto # Maestro contactos
├── batch_P3fV4dWNeMkN5RJMhV8e_tran_deuda     # Transacciones deuda
├── batch_P3fV4dWNeMkN5RJMhV8e_pagos          # Histórico pagos
└── batch_P3fV4dWNeMkN5RJMhV8e_campanas       # Configuración campañas
```

### **📞 Tablas Operativas (Gestiones)**
```
├── mibotair_P3fV4dWNeMkN5RJMhV8e            # Gestiones CALL (humanos)
└── voicebot_P3fV4dWNeMkN5RJMhV8e            # Gestiones VOICEBOT (bot)
```

### **🔧 Tablas de Homologación**
```
├── homologacion_P3fV4dWNeMkN5RJMhV8e_call    # Reglas tipificación CALL
└── homologacion_P3fV4dWNeMkN5RJMhV8e_voicebot # Reglas tipificación VOICEBOT
```

## 🎯 **Objetivos del Dashboard**

- **Productividad de ejecutivos**: Métricas de gestiones por hora, PDPs realizados
- **Contactabilidad**: Tasas de contacto efectivo por ejecutivo, cartera y servicio
- **Seguimiento de compromisos**: Tracking de PDPs y cumplimiento
- **Análisis multi-canal**: Comparativa CALL vs VOICEBOT (Champion Challenge)
- **Atribución de pagos**: ROI por ejecutivo y canal

## 📊 **KPIs Principales**

### **Métricas de Productividad**
- **PDPs por hora**: `gestiones_pdp / (duracion_total_segundos / 3600)`
- **Tasa de contactabilidad**: `(contactos_efectivos / total_gestiones) * 100`
- **Compromisos cumplidos**: `(compromisos_cumplidos / compromisos_total) * 100`
- **Productividad diaria**: `total_gestiones / COUNT(DISTINCT fecha_gestion)`

### **Métricas Multi-Canal (Champion Challenge)**
- **Efectividad CALL**: `contactos_efectivos_call / gestiones_call`
- **Efectividad VOICEBOT**: `contactos_efectivos_bot / gestiones_bot`
- **Lift Post-Bot**: `efectividad_call_post_bot - efectividad_call_frio`

### **Dimensiones de Análisis**
- **Ejecutivo**: Análisis individual por agente (excluyendo 'DISCADOR', 'VOICEBOT')
- **Servicio**: MOVIL vs FIJA (derivado de campo `negocio`)
- **Cartera**: Gestión Temprana, Altas Nuevas, CF, Regular (derivado de `tramo_gestion`)
- **Canal**: CALL vs VOICEBOT (derivado de tabla origen)
- **Zona geográfica**: Distribución territorial
- **Tiempo**: Análisis temporal con granularidades múltiples

## 🏗️ **Arquitectura de Datos - Separada**

```
📊 BigQuery Sources → 🔄 ETL Service → 🗄️ PostgreSQL DWH → 🌐 API Service → ⚛️ Frontend
```

### **Schema Dimensional Implementado**
```sql
-- DIMENSIONES
DIM_TIEMPO, DIM_CLIENTE, DIM_SERVICIO, DIM_CARTERA, DIM_CANAL, DIM_CAMPAÑA

-- HECHOS
FACT_ASIGNACION           # Universo clientes por campaña
FACT_DEUDA_APERTURA       # Snapshot deuda inicial
FACT_GESTIONES            # Actividad agregada por ejecutivo/hora/canal
FACT_GESTIONES_EXPANDIDA  # Detalle por cod_luna + secuencias multi-canal
FACT_PAGOS_ATRIBUIDOS     # Resultados con atribución a gestiones
```

### **Reglas de Negocio Críticas**
- **Un `cod_luna` agrupa múltiples cuentas de diferentes servicios**
- **Gestiones multi-canal**: CALL + VOICEBOT pueden actuar sobre mismo cliente
- **Atribución temporal**: Última gestión antes del pago (ventana 30 días)
- **Ejecutivos automáticos**: CALL sin ejecutivo → 'DISCADOR', VOICEBOT → 'VOICEBOT'

## 🔧 **Configuración Técnica**

### **BigQuery Connection**
- **Project**: `mibot-222814`
- **Dataset**: `BI_USA`
- **Approach**: Multi-table federation con ETL separado
- **Partitioning**: Por fecha en tablas operativas

### **ETL Configuration**
- **Schedule**: Diario a las 2 AM (America/Lima)
- **Integration**: UNION gestiones + JOINs maestros  
- **Data Retention**: 3 años (1095 días)
- **Backfill**: 90 días disponibles

### **Performance Targets**
- **Dashboard load**: <3 segundos
- **Cross-filtering**: <200ms
- **ETL completion**: Antes de 6 AM hora local
- **Concurrent users**: 50 usuarios simultáneos

## 📁 **Archivos de Configuración**

- `config.yaml`: **✅ Configuración principal CORREGIDA con fuentes reales**
- `data_mapping.yaml`: Mapeo de campos BigQuery → dominio estándar
- `homologation_rules.yaml`: Reglas de homologación de tipificaciones
- `dashboard_template.yaml`: Template del dashboard específico

## 🚀 **Setup y Deployment**

### **Validaciones Implementadas**
```bash
# 1. Verificar conectividad BigQuery
python scripts/validate_telefonica_sources.py

# 2. Test estructura de tablas identificadas
python scripts/test_table_schemas.py --client=telefonica-peru

# 3. Validar mapeo de campos
python scripts/validate_field_mapping.py

# 4. Deploy configuración
python scripts/create_telefonica_client.py
```

### **Status de Configuración**
- ✅ **Fuentes de datos**: 8 tablas reales identificadas
- ✅ **Schema validation**: Aprobado
- ✅ **Field mapping**: Completado  
- ✅ **Business rules**: Definidas
- ⏳ **ETL Pipeline**: En desarrollo
- ⏳ **API Integration**: Pendiente
- ⏳ **Dashboard deployment**: Pendiente

## 📈 **SLA y Performance**

- **Dashboard load**: <3 segundos ⏱️
- **Cross-filtering**: <200ms ⚡
- **ETL diario**: Completado antes de 6 AM 🌅
- **Disponibilidad**: 99.9% uptime 🚀
- **Data freshness**: Daily refresh ⚡

## 🔍 **Validación de Datos**

### **Verificaciones Críticas Implementadas**
```sql
-- Trazabilidad pagos → deuda
SELECT COUNT(*) FROM fact_pagos_atribuidos p
LEFT JOIN fact_deuda_apertura d ON p.nro_documento = d.nro_documento
WHERE d.nro_documento IS NULL;

-- Cardinalidad gestiones por canal
SELECT canal, ejecutivo, COUNT(*) as registros
FROM fact_gestiones
GROUP BY canal, ejecutivo
ORDER BY registros DESC;

-- Atribución de pagos por método
SELECT metodo_atribucion, COUNT(*), SUM(monto_pagado)
FROM fact_pagos_atribuidos
GROUP BY metodo_atribucion;
```

## 🏷️ **Metadatos**

- **Version**: 2.0.0 (Fuentes reales identificadas)
- **Issue**: #12 [TELEFONICA-001] 
- **Estado**: ✅ **CONFIGURACIÓN CORREGIDA**
- **Arquitectura**: Hexagonal + ETL separado
- **Schema**: Dimensional con hechos multi-canal
- **Business Owner**: Gerencia de Cobranza Telefónica Perú
- **Technical Owner**: Equipo BI Pulso-AI

---

## 📝 **Change Log**

### **v2.0.0** (2025-06-11) - **CORRECCIÓN CRÍTICA**
- ✅ **Conectado a BigQuery real**
- ✅ **8 tablas reales identificadas** (vs 1 especulativa)
- ✅ **Fuentes operativas separadas**: mibotair + voicebot
- ✅ **Schema dimensional definido**
- ✅ **Reglas de negocio multi-canal**

### **v1.0.0** (2025-06-10) - Configuración inicial especulativa
- ❌ Basado en fuente única especulativa
- ❌ No validado con BigQuery real

**🎯 La configuración ahora refleja la realidad de los datos de Telefónica Perú** ✅