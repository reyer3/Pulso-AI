# 🏢 Clientes (Instancias Multitenant)

**Resumen:** Este directorio alberga configuraciones, adaptaciones y despliegues específicos para cada cliente de la plataforma Pulso-AI. Implementa una estrategia multitenant utilizando un patrón de "Plantilla + Instancias Aisladas" (Template + Isolated Instances), permitiendo que cada cliente tenga una experiencia personalizada pero consistente.

**Propósito Clave y Responsabilidades:**
-   **Aislamiento de Clientes:** Asegurar que los datos, la configuración y el despliegue de cada cliente estén estrictamente aislados.
-   **Personalización:** Permitir configuraciones, adaptadores o variaciones menores de funcionalidad específicas para cada cliente.
-   **Escalabilidad:** Facilitar la incorporación eficiente de nuevos clientes utilizando una plantilla estandarizada.
-   **Gestión:** Proporcionar una estructura clara para administrar múltiples instancias de clientes.

## 🏛️ Arquitectura Multi-Cliente

La idea central es mantener un directorio base `template/` que sirva como modelo para todas las nuevas instancias de clientes. Cada cliente obtiene luego su propio directorio, heredando de la plantilla pero permitiendo modificaciones específicas.

```
clients/
├── template/                 # Modelo base para nuevos servicios de cliente.
│   │                         # Contiene configuraciones base, setup de Docker,
│   │                         # manifiestos de Kubernetes y un README estándar.
│   ├── config/
│   ├── docker-compose.yml
│   ├── k8s/
│   └── README.md
├── cliente-A/                # Ejemplo: Instancia para el Cliente A
│   │                         # (ej., movistar-peru)
│   └── ... (la estructura refleja la plantilla, con modificaciones)
├── cliente-B/                # Ejemplo: Instancia para el Cliente B
│   │                         # (ej., claro-colombia)
│   └── ...
└── README.md                 # Este archivo, explicando el directorio de clientes.
```

## 🔑 Principios de Aislamiento

1.  **Segregación de Datos**: Cada cliente tiene su propia base de datos, esquema o namespace dedicado.
2.  **Independencia de Configuración**: Los ajustes específicos del cliente se gestionan en sus respectivos directorios, sin compartir secretos.
3.  **Autonomía de Despliegue**: El servicio de cada cliente puede ser desplegado, actualizado y escalado independientemente. Diferentes versiones pueden coexistir.
4.  **Monitoreo y Logging**: Logs, métricas y alertas están etiquetados y son filtrables por cliente.

## 🚀 Añadir un Nuevo Cliente

Los nuevos clientes se provisionan típicamente usando un script que copia y personaliza la plantilla `template/`.
```bash
# Ejemplo (comando conceptual)
python scripts/provision_new_client.py <nombre-cliente> --region <region>
```
Este script haría lo siguiente:
1.  Copiar el directorio `clients/template/` a `clients/<nombre-cliente>/`.
2.  Actualizar los valores de marcador de posición en los archivos de configuración.
3.  Inicializar cualquier recurso requerido (ej., esquema de base de datos, buckets S3).

## 📁 Estructura por Cliente

Cada directorio individual de cliente (ej., `clients/cliente-A/`) generalmente sigue esta estructura:
```
<nombre-cliente>/
├── config/                 # Configuraciones específicas del cliente
│   ├── client_settings.yaml  # Ajustes principales, feature flags
│   ├── dimensions.yaml       # Dimensiones y métricas personalizadas
│   └── secrets/              # Marcador para gestión de secretos (ej., Vault, archivos .env - ignorados por git)
├── src/                    # Código fuente para adaptadores o lógica específica del cliente
│   └── adapters/
├── docker-compose.override.yml # Modificaciones para despliegue local con Docker
├── k8s/                    # Manifiestos de Kubernetes adaptados para el cliente
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── README.md               # Documentación específica para esta configuración de cliente.
```

## 🔄 Flujo de Desarrollo

1.  **Primero la Plantilla (Template-First)**: Los cambios genéricos y las nuevas características deberían idealmente añadirse primero a `clients/template/`.
2.  **Sincronización**: Debería existir un mecanismo (script o proceso manual) para propagar los cambios relevantes de la plantilla a los clientes existentes.
3.  **Modificaciones Selectivas**: Los ajustes específicos del cliente se realizan directamente en sus respectivos directorios.
4.  **Pruebas Aisladas**: El entorno de cada cliente debería poder probarse independientemente.

## 📊 Estado del Cliente (Ejemplo)

| Nombre Cliente  | Estado        | Región Clave | Notas                                     |
|-----------------|---------------|--------------|-------------------------------------------|
| `template`      | ✅ Base Activa | N/A          | Plantilla maestra para todos los clientes.|
| `movistar-peru` | 🚧 Desarrollo  | PE           | Cliente piloto inicial.                   |
| `claro-colombia`| 📋 Planeado    | CO           | Esperando configuración.                  |

## 🛡️ Seguridad y Cumplimiento

-   **Acceso Cero a Datos Entre Clientes**: Reforzado a nivel de arquitectura e infraestructura.
-   **Gestión de Secretos**: Utilizar herramientas como HashiCorp Vault o almacenes de secretos específicos del entorno.
-   **Registros de Auditoría**: Todas las acciones significativas y cambios de configuración son rastreables por cliente.
-   **Residencia de Datos**: Asegurar que los datos del cliente se almacenen y procesen de acuerdo con las regulaciones regionales.

---

**Próximos Pasos**: Definir la estructura inicial de `clients/template/` y el script `provision_new_client.py`.
El contenido existente para `movistar-peru`, `claro-colombia`, etc., puede moverse a subdirectorios si ya son instancias de cliente reales. Si son solo ejemplos, el directorio puede limpiarse para contener únicamente `template/` y este README.
```
