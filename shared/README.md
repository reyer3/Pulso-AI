# 🔧 Librerías y Utilidades Compartidas

**Resumen:** Este directorio contiene librerías de Python compartidas, funciones de utilidad, definiciones de tipos comunes y funcionalidades centrales diseñadas para ser utilizadas en múltiples servicios (ej., `core-template`, instancias específicas de clientes) y aplicaciones (ej., `frontend` si se generan SDKs de cliente, `scripts`) dentro del proyecto Pulso-AI. El objetivo principal es promover la reutilización de código (DRY - Don't Repeat Yourself), asegurar la consistencia y centralizar la lógica común.

**Propósito Clave y Responsabilidades:**
-   **Reutilización de Código (DRY):** Proporcionar un lugar central para el código común para evitar la duplicación en diferentes partes del proyecto.
-   **Consistencia:** Asegurar una implementación uniforme de funcionalidades centrales como autenticación, logging, manejo de configuración, etc.
-   **Mantenibilidad:** Simplificar las actualizaciones y correcciones de errores al tener la lógica compartida en un solo lugar.
-   **Abstracción:** Ofrecer abstracciones para tareas comunes como interacción con bases de datos, caché o llamadas a APIs externas.
-   **Intereses Transversales (Cross-Cutting Concerns):** Gestionar aspectos como monitoreo, logging y manejo de excepciones que aplican a múltiples servicios.

## 📁 Estructura del Directorio Explicada

El directorio `shared/` está organizado por dominio funcional:

```
shared/
├── auth/                   # Autenticación, autorización, manejo de JWT, permisos RBAC
│   ├── jwt_handler.py
│   └── permissions.py
├── config/                 # Carga de configuración, gestión de variables de entorno, acceso a secretos
│   ├── base_settings.py
│   └── client_config_loader.py
├── monitoring/             # Configuración de logging, recolección de métricas, utilidades de health check
│   ├── logger.py
│   └── metrics_collector.py
├── utils/                  # Funciones de utilidad general (helpers de base de datos, wrappers de caché, encriptación, validación)
│   ├── db_utils.py
│   └── cache_manager.py
├── exceptions/             # Clases de excepción personalizadas compartidas en toda la aplicación
│   └── common_exceptions.py
├── types/                  # Estructuras de datos comunes, modelos Pydantic o TypedDicts usados entre servicios
│   └── common_models.py
├── communication/          # (Opcional) Clientes para brokers de mensajes (Kafka, RabbitMQ) o servicios gRPC internos
│   └── kafka_producer.py
└── README.md               # Esta documentación
```
*(La estructura detallada existente del README original es excelente y puede adaptarse aquí).*

## 📦 Cómo Usar las Librerías Compartidas

Estas librerías están destinadas a ser utilizadas como paquetes o módulos estándar de Python. Dependiendo de la configuración del proyecto:

-   **Estrategia Monorepo:** Si Pulso-AI está estructurado como un monorepo, los servicios a menudo pueden importar módulos compartidos directamente usando configuraciones de ruta de Python apropiadas (ej., estableciendo `PYTHONPATH` o usando instalaciones editables con `pip install -e ./shared`).
-   **Paquetes Separados:** Alternativamente, cada subdirectorio (o todo el directorio `shared`) podría empaquetarse como un paquete privado de Python e instalarse como una dependencia en otros servicios. Esto es común para proyectos más grandes o cuando los servicios se despliegan independientemente.
    ```bash
    # Ejemplo: en requirements.txt o pyproject.toml de core-template
    # pulso_ai_shared_auth @ git+ssh://git@github.com/reyer3/Pulso-AI.git#subdirectory=shared/auth
    # o si se usa un servidor PyPI privado:
    # pulso-ai-shared-auth = "0.1.0"
    ```

*(Los ejemplos de código detallados existentes para "Autenticación y Autorización", "Monitoreo y Observabilidad", "Utilidades de Base de Datos y Caché", "Gestión de Configuración" y "Tipos Comunes" son excelentes y deberían conservarse en gran medida, quizás bajo encabezados ligeramente más generalizados o como subsecciones que muestren la utilidad de estos módulos compartidos).*

## ✨ Módulos Compartidos Clave (Ejemplos)

### Autenticación (`shared/auth/`)
-   **`jwt_handler.py`**: Gestiona la creación, validación y decodificación de tokens JWT.
-   **`permissions.py`**: Define roles y permisos para RBAC.

### Configuración (`shared/config/`)
-   **`client_config_loader.py`**: Carga configuraciones específicas del cliente desde archivos YAML u otras fuentes.

### Monitoreo (`shared/monitoring/`)
-   **`logger.py`**: Configuración estandarizada de logging estructurado (ej., usando `structlog`).
-   **`metrics_collector.py`**: Utilidades para emitir métricas a Prometheus u otros sistemas de monitoreo.

### Utilidades (`shared/utils/`)
-   **`db_utils.py`**: Patrones abstractos de interacción con bases de datos o helpers específicos para las bases de datos soportadas.
-   **`cache_manager.py`**: Wrapper para mecanismos de caché como Redis.

### Tipos Comunes (`shared/types/`)
-   **`common_models.py`**: Modelos Pydantic o dataclasses para estructuras de datos compartidas (ej., `ClientConfig`, `FilterState`).

## 🤝 Directrices de Contribución

-   Asegurar que el código compartido sea genérico y aplicable a múltiples servicios/contextos.
-   Escribir pruebas unitarias exhaustivas para todas las utilidades y librerías compartidas. La cobertura de pruebas debe ser alta.
-   Documentar funciones y clases claramente con docstrings, explicando su propósito, argumentos y valores de retorno.
-   Mantener la compatibilidad hacia atrás siempre que sea posible, o proporcionar rutas de migración claras si son necesarios cambios que rompan la compatibilidad.
-   Discutir con el equipo antes de añadir nuevas librerías compartidas significativas para asegurar que encajan en la arquitectura general.

---

**Beneficios**:
-   **Reducción de Duplicación**: Escribe una vez, úsalo en todas partes.
-   **Consistencia Mejorada**: Comportamiento uniforme entre servicios.
-   **Mantenimiento Más Fácil**: Corrige errores o añade características en un solo lugar.
-   **Mayor Calidad**: El código compartido tiende a ser más robusto y bien probado.
```
