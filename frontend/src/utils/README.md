# 🛠️ Utilidades del Frontend

**Resumen:** Este directorio almacena diversas funciones de utilidad y helpers que se utilizan en toda la aplicación frontend de Pulso-AI. Estas son típicamente funciones puras que encapsulan lógica común.

**Propósito:**
- Proporcionar un lugar centralizado para funciones de ayuda genéricas, promoviendo la reutilización.
- Mantener el código de los componentes más limpio al delegar tareas comunes (ej., formateo de fechas, transformación de datos, lógica de validación) a funciones de utilidad.
- Mejorar la organización y mantenibilidad del código.
- Facilitar pruebas más sencillas de lógica específica y aislada.

**Contenido Planeado:**
Este directorio puede contener archivos organizados por el tipo de utilidad, por ejemplo:
- `dateUtils.js`: Funciones para formatear, analizar y manipular fechas (ej., `formatDate`, `getTimeAgo`).
- `stringUtils.js`: Funciones para la manipulación de cadenas de texto (ej., `capitalize`, `truncate`).
- `validationUtils.js`: Funciones de validación comunes (ej., `isValidEmail`, `isStrongPassword`).
- `localStorageUtils.js`: Helpers para interactuar con el almacenamiento local (local storage) del navegador.
- `objectUtils.js`: Funciones para la manipulación de objetos (ej., `deepClone`, `isEmptyObject`).
- `arrayUtils.js`: Funciones para la manipulación de arrays (ej., `chunkArray`, `uniqueValues`).
- `apiHelpers.js`: Funciones de utilidad para apoyar las interacciones con la API, como formatear datos de solicitud o manejar respuestas, si no están cubiertas por un hook/servicio de API dedicado.

**Características Clave:**
- **Genéricas:** Las utilidades deben ser lo más genéricas posible, no vinculadas a componentes o características específicas a menos que se nombren explícitamente de esa manera.
- **Funciones Puras:** Preferir funciones puras siempre que sea posible, ya que son más fáciles de probar y razonar.
- **Bien Probadas:** Las funciones de utilidad deben tener una buena cobertura de pruebas unitarias.

**Tecnologías:**
- JavaScript o TypeScript
- Potencialmente librerías como `date-fns` o `lodash` (o funciones específicas de ellas) si se considera necesario, pero apuntar primero a soluciones nativas.

**Directrices de Contribución:**
- Asegurar que las funciones estén bien documentadas, explicando su propósito, parámetros y valores de retorno.
- Escribir pruebas unitarias para todas las funciones de utilidad.
- Evitar añadir funciones excesivamente específicas; considerar si la lógica pertenece en su lugar a un componente o un hook personalizado.
- Agrupar funciones de utilidad relacionadas en archivos con nombres apropiados (ej., `dateUtils.ts`).
```
