# 🏢 Clientes Pulso-AI

Este directorio contiene las instancias específicas de cada cliente, implementando el patrón **Template + Isolated Instances** para multi-tenancy.

## 🎯 Arquitectura Multi-Cliente

```
clients/
├── template/                 # Template base para nuevos clientes
│   ├── config/              # Configuraciones template
│   ├── docker-compose.yml   # Deploy template
│   └── k8s/                 # Manifiestos Kubernetes template
├── movistar-peru/           # Cliente Movistar Perú
├── claro-colombia/          # Cliente Claro Colombia
└── tigo-guatemala/          # Cliente Tigo Guatemala
```

## 🔐 Principios de Aislamiento

1. **Datos completamente aislados**: Cada cliente tiene su propia base de datos/namespace
2. **Configuración independiente**: YAML específico por cliente sin compartir secretos
3. **Deploy independiente**: Cada cliente puede tener versiones diferentes
4. **Monitoreo separado**: Logs y métricas aisladas por cliente

## 🚀 Agregar Nuevo Cliente

```bash
# Usar script de automatización
python scripts/create_client.py nuevo-cliente "Nuevo Cliente SA" \
  --database postgresql --country CO

# Resultado: Estructura completa lista para configurar
```

## 📁 Estructura por Cliente

Cada directorio de cliente sigue esta estructura estándar:

```
cliente-ejemplo/
├── config/
│   ├── client.yaml          # Configuración principal
│   ├── dimensions.yaml      # Dimensiones y métricas
│   ├── database.yaml        # Configuración de BD
│   └── secrets/            # Credenciales (gitignored)
├── src/
│   └── adapters/           # Adaptadores específicos si necesarios
├── docker-compose.yml      # Deploy del cliente
├── k8s/                    # Manifiestos Kubernetes
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── README.md               # Documentación específica
```

## 🔄 Workflow de Desarrollo

1. **Template First**: Todos los cambios van primero al template
2. **Cliente Sync**: Los clientes heredan del template automáticamente
3. **Override Selectivo**: Configuraciones específicas solo cuando es necesario
4. **Testing Isolated**: Cada cliente tiene su propio entorno de testing

## 📊 Clientes Activos

| Cliente | Estado | Base de Datos | Región | URL |
|---------|--------|---------------|--------|-----|
| template | ✅ Base | - | - | - |
| movistar-peru | 🚧 Desarrollo | BigQuery | PE | - |
| claro-colombia | 📋 Planeado | PostgreSQL | CO | - |
| tigo-guatemala | 📋 Planeado | MySQL | GT | - |

## 🛡️ Seguridad y Compliance

- **Zero Cross-Client Access**: Garantizado por arquitectura
- **Secrets Management**: Usando external secrets operator
- **Audit Logging**: Cada acción traceable por cliente
- **Data Residency**: Respeta regulaciones locales por país

---

**Next Steps**: Configurar primer cliente (Movistar Perú) usando el template base.
