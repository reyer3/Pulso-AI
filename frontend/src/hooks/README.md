# 🎣 Hooks Personalizados del Frontend

**Resumen:** Este directorio está designado para Hooks de React personalizados utilizados dentro de la aplicación frontend de Pulso-AI. Estos hooks encapsulan lógica con estado (stateful) reutilizable y efectos secundarios (side effects).

**Propósito:**
- Abstraer la lógica de los componentes en funciones reutilizables.
- Compartir lógica con estado entre múltiples componentes sin usar componentes de orden superior (higher-order components) o render props.
- Simplificar el código de los componentes al delegar lógica compleja a los hooks.
- Mejorar la organización y mantenibilidad del código.

**Contenido Planeado:**
Este directorio contendrá hooks para diversas funcionalidades, tales como:
- `useAuth()`: Manejo del estado de autenticación e información del usuario.
- `useApi(apiRequestFunction, params)`: Hook genérico para realizar llamadas API y manejar estados de carga/error.
- `useForm(initialValues, validationSchema)`: Manejo del estado de formularios, validación y envío.
- `useLocalStorage(key, initialValue)`: Sincronización del estado con el almacenamiento local (local storage) del navegador.
- `useTheme()`: Manejo del tema de la aplicación (modo oscuro/claro).
- `useDebounce(value, delay)`: Retraso controlado de valores (debouncing), útil para entradas de búsqueda.

**Convención de Nomenclatura:**
Todos los hooks personalizados deben comenzar con el prefijo `use` (ej., `useUserData`, `useFormValidation`).

**Tecnologías:**
- React
- TypeScript para seguridad de tipos (type safety).

**Directrices de Contribución:**
- Asegurar que los hooks estén bien documentados, explicando su propósito, parámetros y valores de retorno.
- Escribir pruebas unitarias para los hooks para asegurar que su lógica sea correcta.
- Los hooks deben enfocarse en una única pieza de funcionalidad.
- Evitar hacer hooks excesivamente complejos; componer hooks más pequeños si es necesario.
```
