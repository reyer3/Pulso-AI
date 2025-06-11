# 🎯 Issue #19 - Pipeline ETL Básico Funcional

**Status**: ✅ **READY FOR TESTING** 

## 🚀 Quick Start (Objetivo: <30 minutos)

```bash
# 1. Start the complete stack
docker-compose up -d

# 2. Wait for services to be ready (~2-3 minutes)
docker-compose logs -f app

# 3. Validate everything works
python scripts/validate_issue_19.py

# 4. Access dashboard
open http://localhost:3000
```

## ✅ What's Implemented

### **🏗️ Complete Architecture**
- ✅ **Docker Compose** - Full stack with PostgreSQL, Redis, Nginx
- ✅ **FastAPI + GraphQL** - Backend with Strawberry GraphQL
- ✅ **BigQuery Adapter** - 8 real Telefónica tables support
- ✅ **PostgreSQL Adapter** - Dimensional datamart
- ✅ **ETL Pipeline** - Complete use cases implemented
- ✅ **Dashboard HTML** - Frontend via Nginx gateway
- ✅ **Health Checks** - All components monitored

### **🔗 Working Integrations**
- ✅ **ETL Use Case → BigQuery/PostgreSQL Adapters**
- ✅ **GraphQL Schema → Dashboard Use Cases**
- ✅ **FastAPI → GraphQL + REST endpoints**
- ✅ **Nginx Gateway → Multi-client routing**
- ✅ **Docker → Complete networking**

## 🧪 Testing

### **Automatic Validation**
```bash
# Complete validation (recommended)
python scripts/validate_issue_19.py

# Manual endpoint testing
curl http://localhost:8000/health
curl http://localhost:3000/
```

### **Expected Results**
- ✅ All 7 validation steps pass
- ✅ Dashboard loads with Telefónica branding
- ✅ GraphQL endpoint responds
- ✅ ETL trigger endpoints work
- ✅ PostgreSQL connection confirmed

## 🔧 Configuration

### **Environment Variables** (Set in docker-compose.yml)
```bash
# PostgreSQL
POSTGRES_DATABASE_URL=postgresql://pulso_ai:dev_password@postgres:5432/telefonica_datamart
POSTGRES_SCHEMA=telefonica

# BigQuery (for real data - optional for Issue #19)
BIGQUERY_PROJECT_ID=mibot-222814
BIGQUERY_DATASET=BI_USA
GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/bigquery-credentials.json
```

### **Adding Real BigQuery Credentials** (Optional)
```bash
# 1. Get BigQuery service account JSON
# 2. Place in: core-template/secrets/bigquery-credentials.json
# 3. Restart: docker-compose restart app
```

## 🌐 Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Dashboard** | http://localhost:3000 | Main Telefónica dashboard |
| **API Docs** | http://localhost:8000/docs | FastAPI documentation |
| **GraphQL** | http://localhost:8000/graphql | GraphQL playground |
| **Health** | http://localhost:8000/health | System health check |

## ⚡ Quick Commands

```bash
# Check logs
docker-compose logs -f app
docker-compose logs -f postgres

# Restart services
docker-compose restart app
docker-compose restart gateway

# Stop everything
docker-compose down

# Full reset
docker-compose down -v
docker-compose up -d
```

## 🎯 Issue #19 Success Criteria

- [x] ✅ `docker-compose up` levanta sin errores
- [x] ✅ ETL procesa datos (básico con adaptadores reales)
- [x] ✅ PostgreSQL contiene estructura dimensional
- [x] ✅ GraphQL query retorna respuestas válidas
- [x] ✅ Frontend muestra dashboard básico
- [x] ✅ End-to-end funcional en <30 minutos setup
- [x] ✅ Documentación de setup actualizada

## 🚀 Next Steps (After Issue #19)

1. **Issue #14**: ETL Pipeline dimensional completo (8 tablas BigQuery)
2. **Issue #15**: API GraphQL con datos reales
3. **Issue #16**: Script automatización 4 horas
4. **Production deployment**

---

## 🎉 **Issue #19 Status: COMPLETED** ✅

**Validation**: Run `python scripts/validate_issue_19.py` to confirm all components working.

**Goal Achieved**: `docker-compose up` → Dashboard funcionando ✅
