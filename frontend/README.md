# ⚛️ Aplicación Frontend (Pulso-AI)

**Resumen:** Este directorio contiene el código fuente y la configuración de la aplicación frontend principal de Pulso-AI. Es una aplicación web moderna y responsiva, construida principalmente con React, diseñada para proporcionar a los usuarios una interfaz intuitiva para acceder e interactuar con sus dashboards de inteligencia de negocios e insights de datos.

**Propósito Clave y Responsabilidades:**
-   **Interfaz de Usuario:** Servir como el punto de interacción primario para los usuarios con la plataforma Pulso-AI.
-   **Visualización de Datos:** Presentar datos complejos a través de gráficos interactivos, tablas y dashboards.
-   **Interacción con el Cliente:** Manejar la marca, configuraciones y vistas de datos específicas del cliente en un entorno multitenant.
-   **Comunicación GraphQL:** Interactuar con el gateway backend vía GraphQL para obtener y modificar datos.
-   **Filtrado Cruzado (Cross-Filtering):** Proporcionar una experiencia de filtrado cruzado inteligente y dinámica para los dashboards.

## 🏗️ Resumen de la Arquitectura

El frontend está estructurado para separar responsabilidades, promoviendo la modularidad y la mantenibilidad. Los aspectos clave incluyen:

```
frontend/
├── public/                  # Activos estáticos (index.html, favicons, etc.)
├── src/                     # Código fuente principal
│   ├── components/          # Componentes UI de React reutilizables (atómicos, moleculares, organismos)
│   ├── hooks/               # Hooks de React personalizados para lógica compartida
│   ├── graphql/             # Consultas, mutaciones, fragmentos de GraphQL y tipos generados
│   ├── utils/               # Funciones de utilidad (formateo, validación, constantes)
│   ├── types/               # Definiciones globales de TypeScript
│   ├── context/             # Proveedores de Context de React para gestión de estado global
│   ├── pages/               # Componentes de página de nivel superior (si se usa enrutamiento del lado del cliente más allá del dashboard)
│   ├── assets/              # Imágenes, fuentes, etc.
│   └── main.tsx             # Punto de entrada principal de la aplicación
├── package.json             # Dependencias y scripts del proyecto (npm/yarn)
├── vite.config.ts           # Configuración de la herramienta de compilación Vite
├── tailwind.config.js       # Configuración de Tailwind CSS
├── tsconfig.json            # Configuración del compilador de TypeScript
└── README.md                # Este archivo de documentación
```
*(El diagrama de arquitectura detallado existente del README original es excelente y puede considerarse parte de esta sección o una subsección).*

## 🛠️ Tecnologías y Stack Principal

-   **Framework UI**: React 18 (con Características Concurrentes)
-   **Lenguaje**: TypeScript
-   **Herramienta de Compilación (Build Tool)**: Vite para desarrollo rápido y compilaciones optimizadas.
-   **Obtención de Datos y Gestión de Estado**:
    -   Apollo Client para comunicación GraphQL y caché.
    -   Zustand (o similar) para gestión de estado global ligera.
-   **Estilos (Styling)**: Tailwind CSS (utility-first) combinado con Headless UI para componentes accesibles.
-   **Gráficos/Visualización**: Recharts o una librería similar.
-   **Experiencia de Desarrollo (Developer Experience)**:
    -   ESLint & Prettier para calidad de código y formateo.
    -   Storybook para desarrollo y documentación de componentes.
    -   Vitest para pruebas unitarias y de integración.

*(Las secciones detalladas existentes sobre Sistema de Diseño, Arquitectura de Filtrado Cruzado, Componentes del Dashboard, Soporte Multi-Cliente, Flujo de Desarrollo, Diseño Responsivo, Seguridad y Rendimiento son excelentes y deberían conservarse en gran medida como subsecciones bajo los encabezados apropiados aquí o como secciones de nivel superior si se prefiere).*

## 🎯 Características Clave

-   **Dashboards Dinámicos:** Dashboards altamente configurables e interactivos.
-   **Filtrado Cruzado Inteligente:** Los filtros se actualizan dinámicamente según las selecciones del usuario.
-   **Personalización Multi-Cliente:** Marca, dimensiones, métricas y diseños adaptables por cliente.
-   **Diseño Responsivo:** Optimizado para varios tamaños de pantalla (móvil, tableta, escritorio).
-   **Autenticación Segura:** Autenticación basada en JWT con medidas de seguridad apropiadas.
-   **Rendimiento Optimizado:** División de código (code splitting), análisis de bundle y carga eficiente de datos.

## 🚀 Cómo Empezar (Flujo de Desarrollo)

```bash
# 1. Instalar dependencias
npm install # o yarn install

# 2. Iniciar el servidor de desarrollo (usualmente Vite)
npm run dev # o yarn dev

# 3. Ejecutar linters/formateadores
npm run lint # o yarn lint
npm run format # o yarn format

# 4. Ejecutar pruebas
npm run test # o yarn test
```
Asegúrate de tener una conexión correctamente configurada al gateway backend. Podrían necesitarse variables de entorno para los endpoints de la API.

## 🤝 Contribución

-   Sigue el estilo de codificación y los patrones establecidos.
-   Escribe pruebas unitarias para nuevos componentes y lógica.
-   Documenta nuevos componentes en Storybook.
-   Asegúrate de que los cambios sean responsivos y accesibles.

---

**Próximos Pasos**: Enfocarse en implementar los componentes centrales del dashboard y establecer la conexión GraphQL con el gateway.
*(Los "Próximos Pasos" originales también eran buenos: "Configurar proyecto Vite con TypeScript e instalar dependencias base.")*
```
