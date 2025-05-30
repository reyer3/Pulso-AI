# 📜 Scripts de Automatización y Utilidades

**Resumen:** Este directorio contiene una colección de scripts diseñados para automatizar tareas comunes, optimizar los flujos de trabajo de desarrollo, gestionar la infraestructura y asistir en tareas operativas para el proyecto Pulso-AI. El objetivo principal es mejorar la eficiencia, consistencia y fiabilidad en diversas etapas del ciclo de vida del proyecto.

**Propósito Clave y Responsabilidades:**
-   **Automatización:** Automatizar tareas repetitivas como la incorporación de clientes, despliegues, copias de seguridad y configuración de entornos.
-   **Soporte al Desarrollo:** Proporcionar herramientas para que los desarrolladores simplifiquen la configuración local, pruebas, linting y generación de código.
-   **Integración CI/CD:** Ofrecer scripts que puedan integrarse fácilmente en pipelines de CI/CD para compilaciones, pruebas y despliegues automatizados.
-   **Gestión de Infraestructura:** Ayudar en el aprovisionamiento, escalado y monitoreo de componentes de infraestructura.
-   **Operaciones de Datos:** Facilitar tareas como la sincronización de bases de datos, validación de esquemas y exportaciones de datos.

## 📁 Estructura del Directorio Explicada

Los scripts están organizados por su área funcional:

```
scripts/
├── client-management/      # Scripts para gestionar instancias de clientes (crear, desplegar, backup, migrar)
│   ├── create_client.py
│   └── deploy_client.py
├── development/            # Scripts para ayudar al desarrollo local (configuración, ejecución de pruebas, linting)
│   ├── setup_dev_env.sh
│   └── run_tests.sh
├── cicd/                   # Scripts específicos para uso en pipelines de CI/CD (ej., compilar, publicar)
│   └── build_and_push_docker.sh
├── infrastructure/         # Scripts para gestionar infraestructura (aprovisionamiento, escalado, chequeos de salud)
│   ├── provision_infra.py
│   └── manage_kubernetes_secrets.sh
├── data/                   # Scripts para tareas relacionadas con datos (sincronización de BD, validación de esquemas, exportaciones)
│   └── sync_db.py
├── utils/                  # Scripts de utilidad general o librerías compartidas para otros scripts
│   └── common_utils.py
└── README.md               # Esta documentación
```
*(La estructura detallada existente del README original es excelente y puede adaptarse aquí).*

## 🚀 Categorías Clave de Scripts y Ejemplos

*(Las secciones detalladas existentes: "Scripts Principales" (como `create_client.py`, `deploy_client.py`), "Scripts de Desarrollo", "Scripts de Infraestructura" y "Scripts de Datos" son excelentes. Deberían conservarse, quizás bajo encabezados ligeramente más generalizados si es necesario, pero su nivel actual de detalle es valioso).*

### Gestión de Clientes
-   **`create_client.py`**: Automatiza todo el ciclo de vida de incorporación de un nuevo cliente, desde la creación del directorio hasta el despliegue inicial.
    ```bash
    python scripts/client-management/create_client.py <nombre_cliente> --template <nombre_plantilla>
    ```
-   **`deploy_client.py`**: Maneja el despliegue de servicios específicos del cliente con opciones para entorno, validación y rollback.
    ```bash
    python scripts/client-management/deploy_client.py <nombre_cliente> --env production --validate
    ```

### Desarrollo y CI/CD
-   **`setup_dev_env.sh`**: Configura un entorno de desarrollo local, instala dependencias, configura hooks.
    ```bash
    ./scripts/development/setup_dev_env.sh --with-docker
    ```
-   **`run_tests.sh`**: Ejecuta varios tipos de pruebas (unitarias, integración, e2e) en todo el proyecto o módulos específicos.
    ```bash
    ./scripts/development/run_tests.sh --module core --type integration
    ```

### Infraestructura y Operaciones
-   **`provision_infra.py`**: (Ejemplo) Script para llamar a Terraform u otras herramientas de IaC para aprovisionar recursos para un entorno o cliente específico.
-   **`backup_db.sh`**: Realiza copias de seguridad de bases de datos especificadas.

## 🛠️ Directrices de Uso

-   **Permisos:** Asegúrate de que los scripts sean ejecutables (`chmod +x nombre_script.sh`).
-   **Entorno:** Ten en cuenta el entorno (local, staging, producción) para el que está destinado un script. Muchos scripts pueden requerir que se establezcan variables de entorno específicas (ej., `AWS_PROFILE`, `KUBECONFIG`).
-   **Configuración:** Algunos scripts pueden usar un archivo `config.yaml` compartido o archivos `.env` dentro del directorio `scripts` o la raíz del proyecto para los ajustes. (La sección "Configuración" existente es buena).
-   **Idempotencia:** Siempre que sea posible, los scripts deben diseñarse para ser idempotentes, lo que significa que ejecutarlos varias veces produce el mismo resultado sin efectos secundarios no deseados.
-   **Logging:** Los scripts deben implementar un logging consistente para la trazabilidad y depuración.

## 🤝 Contribuir Nuevos Scripts

-   Coloca el script en el subdirectorio apropiado según su función.
-   Incluye una línea shebang (ej., `#!/bin/bash` o `#!/usr/bin/env python3`).
-   Añade comentarios claros que expliquen la lógica compleja.
-   Proporciona instrucciones de uso, ya sea mediante argumentos `--help` o documentando en este README o en un README de subdirectorio específico.
-   Asegúrate de que cualquier información sensible (claves API, contraseñas) se maneje mediante variables de entorno o un sistema seguro de gestión de secretos, no codificada directamente.
-   Escribe pruebas para scripts complejos si es factible.

---

**Próximos Pasos**: Priorizar la implementación completa y las pruebas de `client-management/create_client.py` y `development/setup_dev_env.sh` para optimizar la configuración inicial del proyecto y la incorporación de clientes.
```
