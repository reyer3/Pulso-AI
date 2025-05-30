# 📋 Template Base para Clientes Pulso-AI

Este es el **template base** que se usa para crear nuevos clientes de forma rápida y consistente.

## 🎯 Propósito

- **Estandarización**: Todos los clientes siguen la misma estructura
- **Velocidad**: Nuevo cliente en 4 horas en lugar de 3 meses
- **Mantenimiento**: Cambios al template se propagan a todos los clientes
- **Calidad**: Configuraciones probadas y validadas

## 📁 Estructura del Template

```
template/
├── config/
│   ├── client.yaml.template     # Configuración principal
│   ├── dimensions.yaml.template # Dimensiones y métricas
│   ├── database.yaml.template   # Configuración de BD
│   └── secrets.yaml.template    # Plantilla de secretos
├── docker-compose.yml.template  # Deploy template
├── k8s/                        # Manifiestos Kubernetes
│   ├── deployment.yaml.template
│   ├── service.yaml.template
│   └── configmap.yaml.template
└── README.md.template           # Documentación del cliente
```

## 🔄 Proceso de Uso

1. **Script Automatizado**: `python scripts/create_client.py`
2. **Reemplazo de Variables**: `{{CLIENT_ID}}`, `{{CLIENT_NAME}}`, etc.
3. **Configuración Específica**: Ajustar dimensiones y métricas
4. **Deploy**: Aplicar configuración K8s/Docker

## 📝 Variables Template

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `{{CLIENT_ID}}` | ID único del cliente | `movistar-peru` |
| `{{CLIENT_NAME}}` | Nombre display | `Movistar Perú` |
| `{{DATABASE_TYPE}}` | Tipo de BD | `bigquery`, `postgresql`, `mysql` |
| `{{COUNTRY_CODE}}` | Código país ISO | `PE`, `CO`, `GT` |
| `{{REGION}}` | Región de deploy | `us-east-1`, `europe-west1` |

## 🛠️ Customización

### Dimensiones Comunes
```yaml
# Estas dimensiones están en la mayoría de clientes
ejecutivo: # Puede ser "agente", "asesor", etc.
  type: categorical
  affects_dimensions: ["cartera", "servicio"]

fecha:
  type: temporal
  granularity: ["day", "week", "month"]

servicio: # Línea de negocio
  type: categorical
  valid_values: ["MOVIL", "FIJA", "HOGAR"]
```

### Métricas Estándar
```yaml
# Métricas que todos los clientes suelen necesitar
tasa_contactabilidad:
  formula: "(contactos / total_gestiones) * 100"
  thresholds: {warning: 30, good: 50}

pdps_por_hora:
  formula: "pdp_count / horas_trabajadas" 
  thresholds: {warning: 2, good: 5}
```

## 🔐 Consideraciones de Seguridad

- **Secrets Separados**: Nunca incluir credenciales en el template
- **Variables de Entorno**: Usar external secrets operator
- **Network Isolation**: Cada cliente en su propio namespace
- **RBAC**: Permisos mínimos necesarios

## 📚 Documentación para Nuevos Clientes

Cada cliente creado a partir del template incluye:

- **Setup Guide**: Cómo configurar el cliente específico
- **Data Mapping**: Correspondencia de campos cliente → Pulso-AI
- **Dashboard Guide**: Cómo usar las visualizaciones
- **Troubleshooting**: Problemas comunes y soluciones

---

**Nota**: Este template se actualiza continuamente. Los clientes existentes pueden optar por sincronizar con la última versión.
