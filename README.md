# 🚀 Pulso-AI: Plataforma BI Multitenant Configurable

**Resumen:** Pulso-AI es una plataforma de Inteligencia de Negocios (BI) de código abierto diseñada para el despliegue rápido de dashboards configurables y multitenant. Aprovecha una arquitectura hexagonal para lograr alta escalabilidad, mantenibilidad y una rápida incorporación de clientes (con el objetivo de reducir la configuración de meses a horas). Este README proporciona una visión general de alto nivel del proyecto, sus objetivos, arquitectura y cómo comenzar.

**Objetivos Clave del Proyecto:**
-   **Incorporación Rápida de Clientes:** Reducir drásticamente el tiempo y el esfuerzo necesarios para desplegar dashboards de BI para nuevos clientes.
-   **Alta Configurabilidad:** Permitir una personalización profunda de dashboards, métricas y dimensiones por cliente mediante archivos de configuración, sin cambios en el código.
-   **Aislamiento Estricto de Datos:** Asegurar una robusta multitenancy donde los datos y la configuración de cada cliente estén completamente aislados.
-   **Interacciones Inteligentes:** Proveer características avanzadas como el filtrado cruzado dinámico (cross-filtering) en los dashboards.
-   **Arquitectura Escalable y Mantenible:** Utilizar un diseño limpio y modular (Arquitectura Hexagonal) para soportar el crecimiento y facilitar el mantenimiento.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](#)
[![GraphQL](https://img.shields.io/badge/GraphQL-Strawberry-purple.svg)](#)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](#)
[![Docker](https://img.shields.io/badge/Docker-Containerization-blue.svg)](#)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-blue.svg)](#)

## 📖 Tabla de Contenidos

- [Resumen del Proyecto y Objetivos](#-pulso-ai-plataforma-bi-multitenant-configurable)
- [El Problema que Resuelve Pulso-AI](#-el-problema-que-resuelve-pulso-ai)
- [Arquitectura Principal](#️-arquitectura-principal)
  - [Flujo de Interacción de Módulos](#-flujo-de-interacción-de-módulos)
- [Características Clave](#-características-clave)
- [Stack Tecnológico](#️-stack-tecnológico)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Cómo Empezar (Guía Rápida)](#-cómo-empezar-guía-rápida)
- [Hoja de Ruta (Roadmap)](#️-hoja-de-ruta-roadmap)
- [Cómo Contribuir](#-cómo-contribuir)
- [Licencia](#-licencia)

## 🤔 El Problema que Resuelve Pulso-AI

Las implementaciones tradicionales de BI para múltiples clientes a menudo implican:
-   Ciclos de desarrollo largos y personalizados por cliente (2-3 meses).
-   Bases de código duplicadas, lo que lleva a desafíos de mantenimiento.
-   Alto riesgo de fuga de datos entre clientes.
-   Escalabilidad difícil.

Pulso-AI aborda esto proporcionando una plataforma central reutilizable y configurable, permitiendo que los dashboards de nuevos clientes se configuren en horas.

## 🏛️ Arquitectura Principal

Pulso-AI se basa en la **Arquitectura Hexagonal** (también conocida como Puertos y Adaptadores o Arquitectura Limpia). Esto asegura una clara separación de responsabilidades, haciendo el sistema modular, testeable y mantenible.

**Componentes Principales y su Interacción:**

```
                                     [ Fuentes de Datos Externas ]
                                         (BigQuery, PostgreSQL, APIs, etc.)
                                                 ↑ ↓ (Adaptadores)
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│ 🏢 CLIENTES               │      │ 🏗️ CORE-TEMPLATE / SERVICIOS│      │ 🔧 LIBRERÍAS COMPARTIDAS  │
│ (Instancias Específicas)  │ ←─── │ (Servicios Hexagonales)   │ ──── │ (Auth, Utils, Config)   │
│ - Configuración y Datos Cliente A│ │ - Dominio (Lógica Negocio)│      └───────────────────────────┘
│ - Configuración y Datos Cliente B│ │ - Aplicación (Casos Uso)│
│ - Usa `core-template`     │      │ - Infraestructura (Adapt.)│
└───────────────────────────┘      │ - API (FastAPI/GraphQL)   │
             ↑                     └───────────────────────────┘
             │ (Configura y Despliega)       ↑ ↓ (API GraphQL)
┌───────────────────────────┐      ┌───────────────────────────┐
│ 📜 SCRIPTS                │      │ 🌐 GATEWAY                │
│ (Automatización, CLI)     │      │ (Nginx, FastAPI)          │
└───────────────────────────┘      │ - Enrutamiento Cliente    │
                                   │ - Auth y Límite Tasa      │
                                   │ - Esquema Dinámico (GraphQL)│
                                   └───────────────────────────┘
                                                 ↑ ↓ (API GraphQL)
                                   ┌───────────────────────────┐
                                   │ ⚛️ FRONTEND                │
                                   │ (Aplicación React)        │
                                   │ - Dashboards, Gráficos    │
                                   │ - UI Filtro Cruzado       │
                                   └───────────────────────────┘

[ 🏗️ INFRAESTRUCTURA (IaC) - Terraform, Kubernetes, Docker ]
(Provisiona y gestiona recursos para todos los componentes)

[ 📚 DOCS - Guías, Arquitectura, ADRs ]
(Documenta todos los aspectos del proyecto)
```

### Flujo de Interacción de Módulos:

1.  **Interacción del Usuario (`Frontend`):** Los usuarios interactúan con el frontend basado en React para ver dashboards y aplicar filtros.
2.  **Llamadas API (`Gateway`):** El frontend se comunica vía GraphQL con el `Gateway`.
3.  **Manejo de Solicitudes (`Gateway`):** El `Gateway` (construido con Nginx/FastAPI) autentica las solicitudes, las enruta según el ID del cliente y las reenvía a la instancia de servicio backend apropiada. Puede usar esquemas GraphQL dinámicos por cliente.
4.  **Lógica de Negocio (Servicios basados en `Core-Template`):** Cada instancia de cliente, construida a partir del `Core-Template`, procesa la solicitud.
    *   La capa `API` en el servicio recibe la llamada.
    *   Los servicios de `Aplicación` orquestan los casos de uso.
    *   La capa de `Dominio` contiene la lógica de negocio pura.
    *   Los adaptadores de `Infraestructura` se conectan a las fuentes de datos (BigQuery, PostgreSQL, etc.) u otros sistemas externos.
5.  **Funcionalidad Compartida (`Shared`):** Lógica común como el manejo de JWT, funciones de utilidad o herramientas de monitoreo personalizadas son utilizadas por varios servicios y scripts.
6.  **Configuración del Cliente (`Clients`):** Cada instancia de cliente en el directorio `clients/` tiene su configuración específica (fuentes de datos, dimensiones, métricas) que dicta su comportamiento. El directorio `clients/template/` proporciona el modelo base.
7.  **Automatización (`Scripts`):** Los scripts CLI automatizan tareas como la creación de nuevas instancias de cliente a partir del template, el despliegue de servicios o la gestión de datos.
8.  **Infraestructura Subyacente (`Infrastructure`):** Todos los componentes se despliegan y gestionan mediante Infraestructura como Código (Terraform, Kubernetes, Docker) definida en el directorio `infrastructure/`.
9.  **Documentación (`Docs`):** El directorio `docs/` contiene toda la documentación relevante para entender, usar y contribuir al proyecto.

*(El diagrama de arquitectura detallado y los principios existentes del README original son excelentes y pueden integrarse aquí o como una subsección).*

## ✨ Características Clave

-   **Configuración Dinámica:** Define dimensiones, métricas y elementos UI por cliente vía YAML.
-   **Filtrado Cruzado Inteligente (Cross-Filtering):** Los filtros se actualizan dinámicamente según las selecciones del usuario en todo el dashboard.
-   **Multitenant por Diseño:** Aísla de forma segura los datos y configuraciones para cada cliente.
-   **Rendimiento Optimizado:** Utiliza Polars para el procesamiento rápido de datos y GraphQL para la obtención eficiente de datos.
-   **Arquitectura Hexagonal:** Asegura la mantenibilidad y escalabilidad.

*(Las descripciones detalladas existentes para estas características son buenas y pueden conservarse).*

## 🛠️ Stack Tecnológico

*(La sección existente del Stack Tecnológico es completa y bien organizada. Debería conservarse tal cual).*
### Backend
- **🐍 Python 3.11+**
- **⚡ FastAPI**
- **📊 Polars**
- **🔍 GraphQL (Strawberry)**
- **🎯 Pydantic**
- **🔄 Celery**
- **📝 SQLAlchemy**

### Frontend  
- **⚛️ React 18**
- **📡 Apollo Client**
- **🎨 Tailwind CSS**
- **📊 Recharts**
- **🏗️ Vite**

### Infraestructura
- **🐳 Docker**
- **☸️ Kubernetes**
- **🌐 Nginx**
- **📈 Prometheus + Grafana**
- **💾 Redis**

### Bases de Datos
- **🏢 BigQuery**
- **🐘 PostgreSQL**
- **🐬 MySQL**

## 📁 Estructura del Proyecto

*(El diagrama de Estructura del Proyecto existente es excelente y debería conservarse, asegurando que refleje todos los directorios principales: `core-template`, `clients`, `gateway`, `frontend`, `scripts`, `infrastructure`, `shared`, `docs`)*.
```
Pulso-AI/
├── 📚 docs/
├── 🏗️ core-template/
├── 🏢 clients/
│   └── template/
├── 🌐 gateway/
├── ⚛️ frontend/
├── 📜 scripts/
├── 🏗️ infrastructure/
├── 🔧 shared/
├── 📋 ROADMAP.md
├── 🐳 docker-compose.yml
└── 📝 README.md
```
(Consulta los READMEs individuales en cada directorio para más detalles sobre su estructura interna.)

## 🚀 Cómo Empezar (Guía Rápida)

*(La sección Cómo Empezar existente es buena y debería conservarse, asegurando que esté actualizada con los procedimientos de configuración actuales).*
### Prerrequisitos
- Python 3.11+
- Docker & Docker Compose
- Node.js 18+

### Pasos
1. Clonar: `git clone https://github.com/reyer3/Pulso-AI.git && cd Pulso-AI`
2. Configurar Backend: `cd core-template && python -m venv venv && source venv/bin/activate && pip install -r requirements/dev.txt && cd ..` (Ajusta la ruta si el backend no es `core-template` en sí mismo sino un servicio construido a partir de él)
3. Configurar Frontend: `cd frontend && npm install && cd ..`
4. Iniciar Servicios: `docker-compose up -d postgres redis` (o similar para servicios core)
5. Ejecutar Backend: `cd core-template && uvicorn src.api.main:app --reload --port 8000 & cd ..` (Ajusta según sea necesario)
6. Ejecutar Frontend: `cd frontend && npm run dev & cd ..`
7. Crear Cliente: `python scripts/client-management/create_client.py demo-client "Demo Client"`
8. Configurar y Desplegar Cliente: Sigue las instrucciones específicas de configuración del cliente.
9. Acceder: Frontend (ej., `http://localhost:5173`), Docs API (ej., `http://localhost:8000/docs`).

## 🗺️ Hoja de Ruta (Roadmap)

Ver [ROADMAP.md](ROADMAP.md) para el plan de desarrollo detallado. Las prioridades clave incluyen:
-   Finalizar el motor principal de filtrado cruzado (cross-filtering).
-   Ampliar el soporte de adaptadores para más fuentes de datos.
-   Mejorar el constructor dinámico de dashboards en el frontend.

## 🤝 Cómo Contribuir

¡Las contribuciones son muy bienvenidas! Nuestro objetivo es crear una comunidad vibrante alrededor de Pulso-AI.
1.  **Leer la Documentación:** Comienza leyendo la documentación en el directorio `docs/`, especialmente `CONTRIBUTING.md` (si está disponible, o esta sección).
2.  **Entender la Arquitectura:** Familiarízate con la Arquitectura Hexagonal y la estructura del proyecto.
3.  **Encontrar un Issue:** Busca issues abiertos en GitHub, especialmente aquellos etiquetados como `good first issue` o `help wanted`.
4.  **Discutir:** Para nuevas características o cambios significativos, por favor abre un issue para discutir tus ideas primero.
5.  **Flujo de Desarrollo:**
    *   Haz un fork del repositorio.
    *   Crea una rama para tu característica: `git checkout -b feature/tu-increible-caracteristica`.
    *   Confirma tus cambios: `git commit -m 'Añade alguna característica increíble'`.
    *   Empuja a la rama: `git push origin feature/tu-increible-caracteristica`.
    *   Abre un Pull Request contra la rama `main` o `develop`.
6.  **Estándares de Código:** Sigue los estilos y convenciones de codificación existentes. Asegúrate de que tu código esté lintado y probado.
7.  **Pruebas (Testing):** Añade pruebas unitarias y de integración para tus cambios.
8.  **Documentación:** Actualiza la documentación relevante si estás cambiando el comportamiento o añadiendo características.

Para directrices detalladas, por favor consulta [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

-   A todos los que han contribuido con ideas y código.
-   Inspirado por la necesidad de democratizar la inteligencia de negocios y hacer accesibles herramientas poderosas.
-   A la comunidad de código abierto por las increíbles herramientas y librerías que hacen posible Pulso-AI.

---

<div align="center">
  <strong>🚀 Pulso-AI: Democratizando la Inteligencia de Negocios</strong><br>
  <em>De 3 meses a 4 horas para la configuración de dashboards de nuevos clientes.</em>
</div>
```
