# 📞 Telefónica del Perú - Configuración Cliente

**Cliente**: Telefónica del Perú (Movistar)  
**Región**: Perú  
**Modelo de negocio**: Gestión de cobranza  
**Fuente principal**: BigQuery (mibot-222814.BI_USA.dash_P3fV4dWNeMkN5RJMhV8e_vw_operativo)

## 🎯 Objetivos del Dashboard

- **Productividad de ejecutivos**: Métricas de gestiones por hora, PDPs realizados
- **Contactabilidad**: Tasas de contacto efectivo por ejecutivo, cartera y servicio
- **Seguimiento de compromisos**: Tracking de PDPs y cumplimiento
- **Análisis multi-canal**: Comparativa CALL vs VOICEBOT

## 📊 KPIs Principales

### Métricas de Productividad
- **PDPs por hora**: `gestiones_pdp / horas_trabajadas`
- **Tasa de contactabilidad**: `(contactos_efectivos / total_gestiones) * 100`
- **Compromisos cumplidos**: `(compromisos_cumplidos / compromisos_total) * 100`
- **Productividad diaria**: `gestiones_realizadas / dias_trabajados`

### Dimensiones de Análisis
- **Ejecutivo**: Análisis individual por agente
- **Servicio**: MOVIL vs FIJA
- **Cartera**: Gestión Temprana, Altas Nuevas, CF, Regular
- **Canal**: CALL vs VOICEBOT
- **Zona geográfica**: Distribución territorial
- **Tiempo**: Análisis temporal (día, semana, mes)

## 🔧 Configuración Técnica

- **BigQuery Project**: `mibot-222814`
- **Dataset**: `BI_USA`
- **Tabla principal**: `dash_P3fV4dWNeMkN5RJMhV8e_vw_operativo`
- **Zona horaria**: `America/Lima`
- **Moneda**: PEN (Soles peruanos)

## 📁 Archivos de Configuración

- `config.yaml`: Configuración principal del cliente
- `data_mapping.yaml`: Mapeo de campos BigQuery → dominio
- `homologation_rules.yaml`: Reglas de homologación de tipificaciones
- `dashboard_template.yaml`: Template del dashboard específico

## 🚀 Setup

Para deployar este cliente, ejecutar:
```bash
python scripts/create_telefonica_client.py
```

## 📈 SLA Performance

- **Dashboard load**: <3 segundos
- **Cross-filtering**: <200ms
- **ETL diario**: Completado antes de 6 AM (hora local)
- **Disponibilidad**: 99.9% uptime
