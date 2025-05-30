# 🌐 API Gateway Pulso-AI

**Gateway central** para routing, autenticación y rate limiting multi-cliente.

## 🎯 Responsabilidades

- **Client Routing**: Enruta requests al cliente correcto
- **Authentication**: JWT validation y autorización
- **Rate Limiting**: Límites per-client configurables
- **Load Balancing**: Distribución de carga entre instancias
- **SSL Termination**: Manejo de certificados SSL/TLS

## 🏗️ Arquitectura

```
Internet
    ↓
🌐 Nginx (Port 80/443)
    ↓
🔀 Load Balancer
    ↓
┌─────────────────────────────────────┐
│ Client Routing Logic                │
│ /movistar-peru/* → Instance 1       │
│ /claro-colombia/* → Instance 2      │
│ /tigo-guatemala/* → Instance 3      │
└─────────────────────────────────────┘
    ↓
🏢 Client-specific Backend Instances
```

## 📁 Estructura

```
gateway/
├── nginx.conf              # Configuración principal Nginx
├── conf.d/                 # Configuraciones por cliente
│   ├── movistar-peru.conf
│   ├── claro-colombia.conf
│   └── tigo-guatemala.conf
├── ssl/                    # Certificados SSL
├── scripts/
│   ├── reload-config.sh    # Recarga configuración
│   └── health-check.sh     # Health check del gateway
├── docker-compose.yml      # Deploy del gateway
└── README.md               # Esta documentación
```

## ⚡ Características

### Client Routing
```nginx
# Ejemplo routing por cliente
location /api/movistar-peru/ {
    proxy_pass http://movistar-backend:8000/;
    proxy_set_header X-Client-ID "movistar-peru";
}
```

### Rate Limiting
```nginx
# Límites por cliente
limit_req_zone $client_id zone=movistar:10m rate=100r/s;
limit_req_zone $client_id zone=claro:10m rate=50r/s;
```

### Load Balancing
```nginx
upstream movistar_backend {
    server movistar-instance-1:8000 weight=3;
    server movistar-instance-2:8000 weight=2;
    health_check;
}
```

## 🔐 Security

- **DDoS Protection**: Rate limiting agresivo
- **Client Isolation**: Headers de identificación
- **Security Headers**: HSTS, CSP, etc.
- **IP Whitelisting**: Por cliente si necesario

---

**Next Steps**: Configurar Nginx con routing básico para desarrollo.
