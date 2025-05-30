# 🏗️ Infrastructure as Code (IaC)

**Terraform** y **Kubernetes** para infrastructure scalable y reproducible.

## 🎯 Filosofía

- **Everything as Code**: Infraestructura versionada y reproducible
- **Multi-Cloud**: Flexibilidad entre proveedores (GCP, AWS, Azure)
- **Environment Parity**: Dev, staging, prod idénticos
- **Auto-Scaling**: Escalamiento automático por demanda

## 📁 Estructura

```
infrastructure/
├── terraform/
│   ├── modules/              # Módulos reutilizables
│   │   ├── kubernetes-cluster/
│   │   ├── database/
│   │   ├── redis/
│   │   └── networking/
│   ├── environments/         # Configuraciones por entorno
│   │   ├── development/
│   │   ├── staging/
│   │   └── production/
│   └── shared/              # Recursos compartidos
├── kubernetes/
│   ├── base/                # Configuraciones base
│   │   ├── namespace/
│   │   ├── rbac/
│   │   ├── network-policies/
│   │   └── storage/
│   ├── overlays/            # Kustomize overlays
│   │   ├── development/
│   │   ├── staging/
│   │   └── production/
│   └── operators/           # Custom operators
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   ├── alertmanager/
│   └── dashboards/
├── database/
│   ├── migrations/          # DB migrations
│   ├── init/               # Initialization scripts
│   └── backup/             # Backup configurations
└── README.md               # Esta documentación
```

## ☸️ Kubernetes Architecture

### Namespaces por Cliente
```yaml
# Aislamiento completo por cliente
apiVersion: v1
kind: Namespace
metadata:
  name: movistar-peru
  labels:
    client: movistar-peru
    environment: production
```

### Resource Quotas
```yaml
# Límites por cliente
apiVersion: v1
kind: ResourceQuota
metadata:
  name: movistar-peru-quota
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"  
    limits.memory: 16Gi
    persistentvolumeclaims: "4"
```

### Network Policies
```yaml
# Aislamiento de red entre clientes
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: client-isolation
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: gateway
```

## 🌍 Terraform Modules

### Kubernetes Cluster
```hcl
# modules/kubernetes-cluster/main.tf
module "gke_cluster" {
  source = "./modules/kubernetes-cluster"
  
  cluster_name     = "pulso-${var.environment}"
  region          = var.region
  node_count      = var.node_count
  machine_type    = var.machine_type
  enable_autoscaling = true
  min_nodes       = 1
  max_nodes       = 10
}
```

### Database per Cliente
```hcl
# modules/database/main.tf
resource "google_sql_database_instance" "client_db" {
  name             = "${var.client_id}-${var.environment}"
  database_version = "POSTGRES_13"
  region          = var.region
  
  settings {
    tier = var.database_tier
    backup_configuration {
      enabled = true
      start_time = "03:00"
    }
  }
}
```

## 📊 Monitoring Stack

### Prometheus Configuration
```yaml
# monitoring/prometheus/config.yaml
global:
  scrape_interval: 15s
  
scrape_configs:
- job_name: 'pulso-backends'
  kubernetes_sd_configs:
  - role: pod
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app]
    action: keep
    regex: pulso-backend
```

### Grafana Dashboards
- **Client Overview**: Métricas por cliente
- **Performance**: Latencia y throughput
- **Infrastructure**: CPU, memoria, storage
- **Business**: KPIs de dashboard usage

## 🔄 CI/CD Pipeline

### GitOps Workflow
```yaml
# .github/workflows/infrastructure.yml
name: Infrastructure
on:
  push:
    paths: ['infrastructure/**']
    
jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: hashicorp/setup-terraform@v2
    - name: Terraform Plan
      run: terraform plan
    - name: Terraform Apply
      if: github.ref == 'refs/heads/main'
      run: terraform apply -auto-approve
```

### ArgoCD for K8s
```yaml
# ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: pulso-infrastructure
spec:
  source:
    repoURL: https://github.com/reyer3/Pulso-AI
    path: infrastructure/kubernetes
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## 🔐 Security

### Secret Management
```yaml
# External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: gcpsm-secret-store
spec:
  provider:
    gcpsm:
      projectId: "pulso-ai-secrets"
      auth:
        workloadIdentity:
          clusterLocation: us-central1
          clusterName: pulso-prod
```

### RBAC per Cliente
```yaml
# Client-specific RBAC
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: movistar-peru
  name: movistar-peru-admin
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "create", "update", "delete"]
```

## 🌐 Multi-Cloud Strategy

### Cloud-Agnostic Modules
```hcl
# Terraform modules that work across clouds
module "database" {
  source = "./modules/database"
  
  provider = var.cloud_provider # "gcp", "aws", "azure"
  instance_type = var.instance_type
  backup_enabled = true
}
```

### Environment Variables
```bash
# Cloud provider selection
export CLOUD_PROVIDER="gcp"              # or "aws", "azure"
export TERRAFORM_BACKEND="gcs"           # or "s3", "azurerm"
export KUBERNETES_PROVIDER="gke"         # or "eks", "aks"
```

## 📈 Auto-Scaling

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pulso-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pulso-backend
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Cluster Autoscaler
```yaml
# Node pool with autoscaling
resource "google_container_node_pool" "pulso_nodes" {
  cluster = google_container_cluster.pulso.name
  
  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }
  
  management {
    auto_repair  = true
    auto_upgrade = true
  }
}
```

## 🔧 Deployment Commands

### Initial Setup
```bash
# 1. Initialize Terraform
cd infrastructure/terraform/environments/production
terraform init

# 2. Plan infrastructure
terraform plan -var-file="terraform.tfvars"

# 3. Apply infrastructure  
terraform apply -auto-approve

# 4. Configure kubectl
gcloud container clusters get-credentials pulso-prod

# 5. Deploy Kubernetes resources
kubectl apply -k infrastructure/kubernetes/overlays/production
```

### Client Onboarding
```bash
# Add new client infrastructure
python scripts/infrastructure/provision_client.py nuevo-cliente \
  --environment production \
  --database postgresql \
  --replicas 3
```

---

**Next Steps**: Configurar cluster base y módulos Terraform para desarrollo.
