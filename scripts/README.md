# 📜 Scripts de Automatización Pulso-AI

**Scripts para automatizar** tareas comunes de desarrollo, deployment y mantenimiento.

## 🎯 Objetivo

Reducir el tiempo de setup de nuevos clientes de **3 meses a 4 horas** mediante automatización completa.

## 📁 Estructura

```
scripts/
├── client-management/
│   ├── create_client.py      # Script principal para crear clientes
│   ├── deploy_client.py      # Deploy automatizado
│   ├── backup_client.py      # Backup de datos de cliente
│   └── migrate_client.py     # Migración entre versiones
├── development/
│   ├── setup_dev.sh          # Setup completo de desarrollo
│   ├── run_tests.sh          # Ejecutar todos los tests
│   ├── lint_all.sh           # Linting de todo el proyecto
│   └── generate_docs.sh      # Generar documentación
├── infrastructure/
│   ├── provision_cluster.py  # Provisionar cluster K8s
│   ├── scale_client.py       # Auto-scaling por cliente
│   └── monitor_health.py     # Monitoring y alertas
├── data/
│   ├── sync_databases.py     # Sincronización de datos
│   ├── validate_schema.py    # Validación de esquemas
│   └── export_analytics.py   # Export de analytics
└── README.md                 # Esta documentación
```

## 🚀 Scripts Principales

### create_client.py
**El script más importante** - crea un cliente completo en minutos.

```bash
# Uso básico
python scripts/create_client.py movistar-peru "Movistar Perú" \
  --database bigquery \
  --country PE \
  --region us-east-1

# Con configuración avanzada
python scripts/create_client.py claro-colombia "Claro Colombia" \
  --database postgresql \
  --country CO \
  --replicas 3 \
  --resources-cpu 2 \
  --resources-memory 4Gi \
  --custom-domain claro.pulso-ai.com
```

**Funcionalidades**:
- ✅ Crea estructura de directorios desde template
- ✅ Reemplaza variables (CLIENT_ID, CLIENT_NAME, etc.)
- ✅ Configura database connections
- ✅ Genera manifiestos K8s
- ✅ Aplica configuración inicial
- ✅ Ejecuta health checks

### deploy_client.py
Deploy automatizado con zero downtime.

```bash
# Deploy a desarrollo
python scripts/deploy_client.py movistar-peru --env development

# Deploy a producción con validaciones
python scripts/deploy_client.py movistar-peru --env production \
  --validate-config \
  --backup-before-deploy \
  --rollback-on-failure
```

### backup_client.py
Backup completo de datos y configuración.

```bash
# Backup completo
python scripts/backup_client.py movistar-peru --include-data

# Solo configuración
python scripts/backup_client.py movistar-peru --config-only
```

## 🛠️ Scripts de Desarrollo

### setup_dev.sh
Setup completo del entorno de desarrollo en un comando.

```bash
# Setup todo el entorno
./scripts/development/setup_dev.sh

# Solo backend
./scripts/development/setup_dev.sh --backend-only

# Solo frontend  
./scripts/development/setup_dev.sh --frontend-only
```

**Funcionalidades**:
- Instala dependencies Python y Node.js
- Configura pre-commit hooks
- Levanta servicios Docker
- Ejecuta tests iniciales
- Valida que todo funciona

### run_tests.sh
Ejecuta todos los tests con coverage.

```bash
# Todos los tests
./scripts/development/run_tests.sh

# Solo backend
./scripts/development/run_tests.sh --backend

# Solo tests E2E
./scripts/development/run_tests.sh --e2e
```

## 🏗️ Scripts de Infraestructura

### provision_cluster.py
Provisiona un cluster Kubernetes completo.

```bash
# Cluster básico
python scripts/infrastructure/provision_cluster.py --name pulso-dev

# Cluster con monitoring
python scripts/infrastructure/provision_cluster.py --name pulso-prod \
  --monitoring \
  --backup \
  --multi-region
```

### scale_client.py  
Auto-scaling inteligente por cliente.

```bash
# Escalar basado en métricas
python scripts/infrastructure/scale_client.py movistar-peru --auto

# Escalar manualmente
python scripts/infrastructure/scale_client.py movistar-peru --replicas 5
```

## 📊 Scripts de Datos

### sync_databases.py
Sincronización de datos entre entornos.

```bash
# Sync dev -> staging
python scripts/data/sync_databases.py movistar-peru \
  --from development --to staging

# Solo schema (sin datos)
python scripts/data/sync_databases.py movistar-peru \
  --schema-only
```

### validate_schema.py
Validación de esquemas de datos.

```bash
# Validar cliente específico
python scripts/data/validate_schema.py movistar-peru

# Validar todos los clientes
python scripts/data/validate_schema.py --all-clients
```

## 🔄 Workflow Típico

### Nuevo Cliente (4 horas)
```bash
# 1. Crear cliente (5 min)
python scripts/create_client.py nuevo-cliente "Nuevo Cliente SA"

# 2. Configurar dimensiones y métricas (2 horas)
# Editar: clients/nuevo-cliente/config/

# 3. Deploy a desarrollo (10 min)
python scripts/deploy_client.py nuevo-cliente --env development

# 4. Validar y ajustar (1.5 horas)
# Testing y fine-tuning

# 5. Deploy a producción (10 min)
python scripts/deploy_client.py nuevo-cliente --env production
```

### Desarrollo Diario
```bash
# Setup diario
./scripts/development/setup_dev.sh --quick

# Desarrollo...

# Antes de commit
./scripts/development/lint_all.sh
./scripts/development/run_tests.sh --quick
```

## 🔐 Configuración

### Variables de Entorno
```bash
# Credenciales de cloud
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."

# Configuración de clusters
export KUBERNETES_CLUSTER="pulso-prod"
export DOCKER_REGISTRY="gcr.io/pulso-ai"

# Notificaciones
export SLACK_WEBHOOK_URL="..."
export EMAIL_SMTP_CONFIG="..."
```

### Configuración Scripts
```yaml
# scripts/config.yaml
default_settings:
  backup_retention_days: 30
  health_check_timeout: 60
  deploy_timeout: 300
  
client_defaults:
  replicas: 2
  cpu_limit: "1000m"
  memory_limit: "2Gi"
  storage_size: "10Gi"
```

## 📈 Monitoring y Alertas

Los scripts incluyen monitoring automático:

- **Slack notifications** en deploy success/failure
- **Email alerts** para errores críticos  
- **Logs centralizados** en todos los scripts
- **Metrics collection** para tiempos de ejecución

---

**Next Steps**: Implementar create_client.py como script prioritario para la Fase 1.
