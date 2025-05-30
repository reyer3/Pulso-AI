# 📄 Requisitos del Core-Template

**Resumen:** Este directorio contiene los archivos de requisitos de dependencias de Python para el servicio `core-template`. Estos archivos son utilizados por `pip` para gestionar las dependencias del proyecto.

**Propósito:**
- Definir y gestionar las dependencias necesarias para que el `core-template` funcione correctamente.
- Separar las dependencias base de las dependencias específicas de desarrollo, permitiendo entornos optimizados.

**Estructura de Archivos:**
- `base.txt`: Especifica las librerías fundamentales esenciales para la funcionalidad de la aplicación en cualquier entorno (desarrollo, pruebas, producción).
- `dev.txt`: Enumera dependencias adicionales útiles solo durante el desarrollo, como frameworks de pruebas, linters y formateadores de código. Este archivo típicamente incluye `base.txt`.

**Uso:**
Para instalar dependencias:
```bash
# Instalar dependencias base
pip install -r base.txt

# Instalar dependencias de desarrollo (que usualmente incluye las base)
pip install -r dev.txt
```
