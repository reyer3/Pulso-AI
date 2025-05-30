# 🏗️ Plantilla Base de Servicio (Core Template)

**Resumen:** Este directorio contiene la plantilla fundamental para crear nuevos servicios backend dentro del ecosistema Pulso-AI. Está diseñada en torno a los principios de la Arquitectura Hexagonal (también conocida como Puertos y Adaptadores o Arquitectura Limpia) para asegurar una clara separación de responsabilidades, mantenibilidad y testabilidad.

**Propósito Clave y Responsabilidades:**
-   **Estandarización:** Proporcionar una estructura y un patrón arquitectónico consistentes para todos los servicios backend.
-   **Reusabilidad:** Permitir el desarrollo rápido de nuevos servicios ofreciendo un esqueleto preconfigurado.
-   **Mantenibilidad:** Promover una arquitectura limpia que aísle la lógica de negocio de la infraestructura y los mecanismos de entrega.
-   **Testabilidad:** Facilitar las pruebas unitarias, de integración y de extremo a extremo (end-to-end) definiendo claramente los límites entre componentes.

## 🏛️ Implementación de la Arquitectura Hexagonal

El `core-template` materializa la Arquitectura Hexagonal, que estructura la aplicación en capas distintas:

-   **Dominio (Núcleo):** Contiene la lógica de negocio pura, entidades e interfaces de casos de uso (puertos). No tiene dependencias de ninguna otra capa.
-   **Aplicación:** Orquesta los casos de uso (servicios de aplicación) implementando los puertos del dominio. Depende únicamente de la capa de Dominio.
-   **Infraestructura:** Proporciona implementaciones concretas para las interfaces definidas en la capa de Dominio (adaptadores para bases de datos, APIs externas, etc.). Depende de las capas de Dominio y Aplicación (para implementar interfaces y ser llamada por los servicios de aplicación).
-   **API (Mecanismo de Entrega):** Expone la funcionalidad de la aplicación a través de una API (ej., REST, GraphQL). Actúa como un punto de entrada y traduce las solicitudes a llamadas de servicios de aplicación.

```
Sistemas Externos (Bases de Datos, APIs de Terceros)
       ↑ ↓
[ Adaptadores de Infraestructura ] ←─────┐
       ↑ ↓                               │ (implementa)
[   Servicios de Aplicación    ] ─────→ [ Lógica de Dominio y Puertos ]
       ↑ ↓                               │ (define)
[ API (FastAPI/GraphQL) ] ←───────────────┘
       ↑ ↓
   Clientes (Frontend, Gateway)
```

## 📁 Estructura del Directorio Explicada

La plantilla está organizada de la siguiente manera:

```
core-template/
├── src/                    # Código fuente del servicio
│   ├── domain/             # 💼 Lógica de Negocio: Entidades, Objetos de Valor, Servicios de Dominio, Interfaces de Repositorio (Puertos). Python puro, sin dependencias de frameworks.
│   ├── application/        # 🔄 Casos de Uso: Servicios de aplicación que orquestan la lógica de dominio. Implementa los puertos de dominio.
│   ├── infrastructure/     # 🔌 Adaptadores e Implementaciones: Implementaciones concretas de interfaces de repositorio (ej., interacciones con base de datos), clientes de servicios externos, productores/consumidores de colas de mensajes.
│   └── api/                # 🌐 Capa de API: Aplicación FastAPI, esquemas GraphQL (Strawberry), modelos de solicitud/respuesta (Pydantic), configuración de inyección de dependencias.
├── tests/                  # 🧪 Pruebas: Organizadas reflejando la estructura de src/ (unitarias, integración, e2e).
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── requirements/           # 📦 Dependencias de Python: Separadas en base.txt (núcleo) y dev.txt (herramientas de desarrollo).
│   ├── base.txt
│   └── dev.txt
├── pytest.ini              # Configuración para Pytest.
└── README.md               # Esta documentación.
```

## ✨ Principios Arquitectónicos Clave

1.  **Separación de Responsabilidades**: Cada capa tiene una responsabilidad distinta y bien definida.
2.  **Inversión de Dependencias**: Las dependencias fluyen hacia adentro. La capa de Dominio es independiente. Las capas de Infraestructura y API dependen de abstracciones definidas en las capas de Dominio/Aplicación.
3.  **Interfaces Explícitas (Puertos y Adaptadores)**: La comunicación entre capas ocurre a través de interfaces bien definidas (puertos) y sus implementaciones (adaptadores).
4.  **Testabilidad**: Cada capa puede ser probada independientemente. La lógica de dominio puede ser probada unitariamente sin dependencias externas.

## 🚀 Cómo Usar Esta Plantilla

1.  **Copiar**: Duplica el directorio `core-template/` para un nuevo servicio (ej., `services/nuevo-servicio/`).
2.  **Renombrar/Refactorizar**: Ajusta los nombres (ej., nombres de módulos, nombres de clases) para reflejar el contexto delimitado del nuevo servicio.
3.  **Configurar**: Define configuraciones específicas (conexiones de base de datos, claves API) típicamente mediante variables de entorno o archivos de configuración cargados por la capa de infraestructura.
4.  **Implementar**:
    *   Define entidades y lógica de dominio en `src/domain/`.
    *   Crea servicios de aplicación en `src/application/`.
    *   Construye adaptadores para sistemas externos en `src/infrastructure/`.
    *   Expón la funcionalidad a través de `src/api/`.
5.  **Probar**: Escribe pruebas exhaustivas para todas las capas.

## 🛠️ Tecnologías y Patrones

-   **Framework Backend**: Python 3.11+, FastAPI (asíncrono)
-   **GraphQL**: Strawberry para Python
-   **Manejo de Datos**: Polars (para manipulación de datos de alto rendimiento, si aplica), Pydantic (para validación y serialización)
-   **Patrones Arquitectónicos**: Arquitectura Hexagonal, Patrón Repositorio, Inyección de Dependencias, CQRS (opcional, donde sea apropiado).
-   **Pruebas**: Pytest, `httpx` (para pruebas de API).

## 📝 Convenciones

(El contenido existente sobre Nomenclatura, Imports y Documentación es bueno y se conserva)
### Nomenclatura (Naming)
- **Clases**: PascalCase (`ClienteService`)
- **Funciones**: snake_case (`generate_dashboard`)
- **Archivos**: snake_case (`client_repository.py`)
- **Directorios**: kebab-case (`cross-filtering/`)

### Imports
```python
# Orden de imports
import standard_library
import third_party
import local_modules
```

### Documentación
```python
def process_client_data(client_id: str) -> DashboardData:
    """Procesa datos del cliente para dashboard.
    
    Args:
        client_id: Identificador único del cliente
        
    Returns:
        Datos procesados listos para visualización
        
    Raises:
        ClientNotFoundError: Si el cliente no existe
    """
```

## 🔄 Ciclo de Desarrollo

(El contenido existente es bueno y se conserva)
1. **Desarrollo de Características**: En core-template
2. **Pruebas**: Pruebas unitarias + integración
3. **Despliegue**: A cliente de pruebas
4. **Validación**: Con datos reales
5. **Lanzamiento (Rollout)**: A todos los clientes existentes

## 🤝 Directrices de Contribución

(El contenido existente es bueno y se conserva)
Para contribuir al core:

1. **Rama (Branch)**: `feature/core-feature-name`
2. **Pruebas (Tests)**: Cobertura > 85%
3. **Documentación (Docs)**: Actualizar si es necesario
4. **Migración**: Plan para clientes existentes

---

*Esta plantilla es el corazón de los servicios backend de Pulso-AI: una base sólida para construir aplicaciones escalables, mantenibles y testeables.*
```
