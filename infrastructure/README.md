# 🏗️ Infraestructura como Código (IaC) - Pulso-AI

**Resumen:** Este directorio contiene todas las configuraciones de Infraestructura como Código (IaC) para la plataforma Pulso-AI. Define, provisiona y gestiona la infraestructura subyacente utilizando herramientas como Terraform para recursos en la nube y Kubernetes (Kustomize) para la orquestación de aplicaciones. También incluye configuraciones para entornos de desarrollo local utilizando Docker Compose.

**Propósito Clave y Responsabilidades:**
-   **Aprovisionamiento Automatizado:** Definir y automatizar la configuración de todos los recursos de la nube (redes, cómputo, bases de datos, etc.).
-   **Consistencia de Entornos:** Asegurar la paridad entre los entornos de desarrollo, staging y producción a través del código.
-   **Escalabilidad y Reproducibilidad:** Permitir una infraestructura escalable que pueda ser reproducida de manera fiable y versionada.
-   **Orquestación:** Gestionar despliegues de aplicaciones contenerizadas, escalado y redes utilizando Kubernetes.
-   **Desarrollo Local:** Proporcionar archivos Docker Compose para simular entornos de nube para desarrollo y pruebas locales.
-   **Infraestructura de Monitoreo y Logging:** Definir la configuración para las pilas de monitoreo, logging y alertas.

## 🏛️ Tecnologías Principales

-   **Terraform:** Utilizado para aprovisionar y gestionar recursos de infraestructura en la nube a través de varios proveedores (GCP, AWS, Azure).
    -   **Módulos:** Configuraciones de Terraform reutilizables para componentes comunes (ej., clústeres de Kubernetes, bases de datos).
    -   **Entornos:** Configuraciones separadas para `development` (desarrollo), `staging` (pruebas) y `production` (producción).
-   **Kubernetes (K8s):** Utilizado para orquestar aplicaciones contenerizadas.
    -   **Kustomize:** Para gestionar configuraciones de Kubernetes específicas del entorno superponiendo cambios sobre una base común.
    -   **Helm Charts (Opcional):** Para empaquetar y desplegar aplicaciones de terceros o servicios internos complejos.
-   **Docker & Docker Compose:** Utilizado para contenerizar aplicaciones y configurar entornos de desarrollo local que replican las configuraciones de producción.
-   **Ansible (Opcional):** Para tareas de gestión de configuración si es necesario para máquinas virtuales o configuraciones de software específicas no cubiertas por Terraform/K8s.

## 📁 Estructura del Directorio Explicada

```
infrastructure/
├── terraform/                    # Configuraciones de Terraform
│   ├── modules/                  # Módulos de Terraform reutilizables (ej., vpc, kubernetes_cluster, database)
│   ├── environments/             # Configuraciones específicas del entorno (dev, staging, prod)
│   │   ├── development/
│   │   ├── staging/
│   │   └── production/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── backend.tf      # Configuración del backend de estado de Terraform
│   └── shared/                   # Recursos compartidos o configuraciones base
├── kubernetes/                   # Manifiestos de Kubernetes y configuraciones de Kustomize
│   ├── base/                     # Manifiestos base comunes para todos los entornos
│   │   ├── core-template-deployment.yaml
│   │   ├── gateway-service.yaml
│   │   └── namespace.yaml
│   ├── overlays/                 # Superposiciones (overlays) de Kustomize específicas del entorno
│   │   ├── development/          # Parches para dev
│   │   ├── staging/              # Parches para staging
│   │   └── production/           # Parches para prod
│   └── operators/                # Operadores de Kubernetes personalizados desarrollados para Pulso-AI
├── docker-compose/               # Archivos Docker Compose para entornos locales/CI
│   ├── docker-compose.yml        # Configuración base de desarrollo local
│   ├── docker-compose.ci.yml     # Configuración para pruebas CI
│   └── .env.example              # Variables de entorno de ejemplo para Docker Compose
├── monitoring/                   # Configuración para monitoreo, logging y alertas
│   ├── prometheus/               # Configuraciones de Prometheus, trabajos de scrapeo
│   ├── grafana/                  # Definiciones de dashboards de Grafana (como código)
│   ├── alertmanager/             # Configuraciones de Alertmanager
│   └── loki/                     # Configuraciones de Loki para agregación de logs (si se usa)
├── database/                     # Scripts específicos de base de datos, ej. migraciones avanzadas
│   ├── migrations/               # Scripts de migración de esquema (ej., Flyway, Alembic - si no son parte de la app)
│   └── init-scripts/             # Scripts de inicialización para bases de datos
└── README.md                     # Esta documentación
```
*(Las secciones detalladas existentes sobre Filosofía de IaC, Arquitectura de Kubernetes, Módulos de Terraform, Pila de Monitoreo, CI/CD, Seguridad, Multi-Nube, Auto-Escalado y Comandos de Despliegue son excelentes y deberían conservarse en gran medida e integrarse bajo encabezados relevantes o como secciones de nivel superior si encajan en el flujo).*

## 🚀 Cómo Empezar y Despliegue

-   **Terraform:**
    ```bash
    cd infrastructure/terraform/environments/<tu-entorno>
    terraform init
    terraform plan
    terraform apply
    ```
-   **Kubernetes (con Kustomize):**
    ```bash
    kubectl apply -k infrastructure/kubernetes/overlays/<tu-entorno>
    ```
-   **Docker Compose (para desarrollo local):**
    ```bash
    cd infrastructure/docker-compose
    docker-compose -f docker-compose.yml up -d
    ```

Consulta los READMEs específicos dentro de los subdirectorios (ej., `terraform/README.md`, `kubernetes/README.md`) para instrucciones más detalladas.

## 🛡️ Consideraciones de Seguridad

-   **Gestión de Secretos:** Utilizar herramientas como HashiCorp Vault, gestores de secretos del proveedor de nube (ej., GCP Secret Manager, AWS Secrets Manager) o el operador ExternalSecrets de Kubernetes. Los secretos no deben estar codificados (hardcoded) en los archivos de IaC.
-   **Seguridad de Red:** Implementar políticas de red estrictas, firewalls y configuraciones de VPC.
-   **RBAC (Control de Acceso Basado en Roles):** Aplicar el acceso de menor privilegio tanto para los componentes de infraestructura como para las cargas de trabajo de Kubernetes.
-   **Escaneo de IaC:** Integrar herramientas como `tfsec`, `checkov` o `terrascan` en los pipelines de CI/CD para escanear en busca de configuraciones erróneas.

---

**Próximos Pasos**: Desarrollar los módulos iniciales de Terraform para la red principal y un clúster GKE/EKS. Definir las configuraciones base de Kustomize para el servicio `core-template` y el `gateway`.
```
