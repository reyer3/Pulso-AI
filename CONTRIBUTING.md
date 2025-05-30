# 🤝 Contributing to Pulso-AI

¡Gracias por tu interés en contribuir a Pulso-AI! Este documento te guiará a través del proceso de contribución.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Setup de Desarrollo](#setup-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar Issues](#reportar-issues)
- [Roadmap y Prioridades](#roadmap-y-prioridades)

## 📜 Código de Conducta

Este proyecto sigue el [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Al participar, te comprometes a mantener un ambiente respetuoso y profesional.

## 🚀 ¿Cómo puedo contribuir?

### 🐛 Reportando Bugs
- Usa los [issue templates](.github/ISSUE_TEMPLATE/)
- Incluye información detallada del entorno
- Provee pasos claros para reproducir
- Adjunta logs y screenshots cuando sea posible

### 💡 Sugiriendo Features
- Revisa el [roadmap](ROADMAP.md) primero
- Crea un issue con label `enhancement`
- Describe el problema que resuelve
- Incluye mockups o ejemplos si es posible

### 🔧 Contribuyendo Código
- Busca issues con label `good first issue` para empezar
- Comenta en el issue antes de comenzar a trabajar
- Sigue las [convenciones de código](#estándares-de-código)
- Incluye tests para todo código nuevo

### 📚 Mejorando Documentación
- Typos, clarificaciones, ejemplos adicionales
- Tutoriales y guías de uso
- Documentación de APIs
- Traducciones (próximamente)

## 🛠️ Setup de Desarrollo

### Prerequisitos
```bash
# Versiones requeridas
Python 3.11+
Node.js 18+
Docker & Docker Compose
Git 2.25+
```

### 1. Fork y Clone
```bash
# Fork el repositorio en GitHub
git clone https://github.com/TU_USERNAME/Pulso-AI.git
cd Pulso-AI

# Agregar upstream remote
git remote add upstream https://github.com/reyer3/Pulso-AI.git
```

### 2. Setup Backend
```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements/dev.txt
```

### 3. Setup Frontend
```bash
cd frontend
npm install
```

### 4. Setup Infrastructure
```bash
# Servicios de desarrollo
docker-compose up -d postgres redis

# Verificar que todo funciona
docker-compose ps
```

### 5. Pre-commit Hooks
```bash
# Instalar pre-commit hooks
pre-commit install

# Probar hooks
pre-commit run --all-files
```

### 6. Verificar Setup
```bash
# Backend tests
cd backend
pytest

# Frontend tests  
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 📏 Estándares de Código

### Python (Backend)

#### Formato y Linting
```bash
# Formateo automático
black .
isort .

# Linting
flake8
mypy src/

# Ejecutar todos los checks
make lint
```

#### Convenciones
- **PEP 8** para style guide
- **Type hints** obligatorios
- **Docstrings** para clases y funciones públicas
- **Máximo 88 caracteres** por línea (black default)

#### Ejemplo de Código
```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ClientConfig:
    """Configuración específica del cliente.
    
    Attributes:
        client_id: Identificador único del cliente
        name: Nombre display del cliente
        dimensions: Lista de dimensiones configuradas
    """
    client_id: str
    name: str
    dimensions: List[DimensionConfig]
    
    def validate(self) -> bool:
        """Valida la configuración del cliente.
        
        Returns:
            True si la configuración es válida
            
        Raises:
            ValidationError: Si la configuración es inválida
        """
        if not self.client_id:
            raise ValidationError("client_id es requerido")
        return True
```

### TypeScript (Frontend)

#### Configuración
- **ESLint + Prettier** para formato
- **TypeScript strict mode**
- **Import ordering** automático

#### Convenciones
```typescript
// Interfaces con PascalCase
interface DashboardProps {
  clientId: string;
  onFilterChange: (filters: FilterState[]) => void;
}

// Componentes con PascalCase
export function Dashboard({ clientId, onFilterChange }: DashboardProps) {
  // Hooks al inicio
  const [filters, setFilters] = useState<FilterState[]>([]);
  const { data, loading } = useQuery(DASHBOARD_QUERY);
  
  // Funciones con camelCase
  const handleFilterChange = useCallback((newFilters: FilterState[]) => {
    setFilters(newFilters);
    onFilterChange(newFilters);
  }, [onFilterChange]);
  
  // Early returns para loading/error states
  if (loading) return <DashboardSkeleton />;
  if (!data) return <ErrorMessage />;
  
  return (
    <div className="dashboard">
      {/* JSX aquí */}
    </div>
  );
}
```

### Testing

#### Backend Tests
```python
# tests/test_dashboard_service.py
import pytest
from unittest.mock import Mock

class TestDashboardService:
    def test_generate_dashboard_success(self):
        # Arrange
        mock_repo = Mock()
        service = DashboardService(mock_repo)
        
        # Act
        result = service.generate_dashboard("client-1", [])
        
        # Assert
        assert result.client_id == "client-1"
        mock_repo.get_data.assert_called_once()
```

#### Frontend Tests
```typescript
// components/__tests__/Dashboard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { MockedProvider } from '@apollo/client/testing';
import { Dashboard } from '../Dashboard';

const mocks = [
  {
    request: { query: DASHBOARD_QUERY },
    result: { data: { dashboardData: [] } }
  }
];

test('renders dashboard with filters', async () => {
  render(
    <MockedProvider mocks={mocks}>
      <Dashboard clientId="test-client" />
    </MockedProvider>
  );
  
  expect(screen.getByText('Dashboard')).toBeInTheDocument();
});
```

## 🔄 Proceso de Pull Request

### 1. Crear Branch
```bash
# Siempre desde main actualizado
git checkout main
git pull upstream main

# Crear feature branch
git checkout -b feature/amazing-feature
# o
git checkout -b fix/bug-description
```

### 2. Desarrollo
```bash
# Commits frecuentes con mensajes descriptivos
git add .
git commit -m "feat: add cross-filtering engine"

# Seguir conventional commits
feat: nueva feature
fix: bug fix
docs: cambios en documentación
style: formato, no funcional
refactor: refactoring
test: agregar tests
chore: tareas de mantenimiento
```

### 3. Pre-PR Checklist
- [ ] Código formateado (`make lint`)
- [ ] Tests pasan (`make test`)
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado (si aplica)
- [ ] No hay merge conflicts

### 4. Crear Pull Request
```bash
# Push del branch
git push origin feature/amazing-feature

# Crear PR en GitHub con:
# - Título descriptivo
# - Descripción detallada
# - Link a issue relacionado
# - Screenshots si aplica
```

### 5. Template de PR
```markdown
## Descripción
Descripción clara de los cambios realizados.

## Tipo de Cambio
- [ ] Bug fix (no breaking change)
- [ ] Nueva feature (no breaking change)  
- [ ] Breaking change (fix o feature que causa que funcionalidad existente no funcione como esperado)
- [ ] Cambio de documentación

## ¿Cómo se ha probado?
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Tests manuales

## Checklist
- [ ] Mi código sigue las convenciones del proyecto
- [ ] He realizado self-review de mi código
- [ ] He comentado mi código en áreas complejas
- [ ] He actualizado la documentación correspondiente
- [ ] Mis cambios no generan nuevas warnings
- [ ] He agregado tests que prueban mi fix/feature
- [ ] Tests unitarios nuevos y existentes pasan localmente
```

## 🐛 Reportar Issues

### Issue Templates

#### Bug Report
```markdown
**Describe el bug**
Descripción clara del problema.

**Para Reproducir**
Pasos para reproducir:
1. Ir a '...'
2. Click en '....'
3. Scroll down a '....'
4. Ver error

**Comportamiento Esperado**
Descripción clara de qué esperabas que pasara.

**Screenshots**
Si aplica, agrega screenshots para explicar el problema.

**Información del Entorno:**
 - OS: [e.g. iOS]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]
 - Python version
 - Node version

**Contexto Adicional**
Cualquier otra información relevante.
```

#### Feature Request
```markdown
**¿Tu feature request está relacionada a un problema?**
Descripción clara del problema. Ej. Estoy siempre frustrado cuando [...]

**Describe la solución que te gustaría**
Descripción clara de qué quieres que pase.

**Describe alternativas que has considerado**
Descripción de soluciones o features alternativas.

**Contexto Adicional**
Contexto o screenshots adicionales sobre el feature request.
```

### Labels y Prioridades

#### Labels de Tipo
- `bug`: Algo no funciona correctamente
- `enhancement`: Nueva feature o request
- `documentation`: Mejoras en documentación
- `question`: Pregunta sobre el proyecto

#### Labels de Prioridad  
- `priority: high`: Crítico, bloquea desarrollo
- `priority: medium`: Importante, pero no bloquea
- `priority: low`: Nice to have

#### Labels de Estado
- `status: triage`: Necesita revisión inicial
- `status: ready`: Listo para trabajar
- `status: in-progress`: Alguien está trabajando en esto
- `status: blocked`: Bloqueado por dependencias

#### Labels Especiales
- `good first issue`: Perfecto para nuevos contributors
- `help wanted`: Se necesita ayuda de la community
- `breaking change`: Cambio que rompe compatibilidad

## 🗺️ Roadmap y Prioridades

### Fases Actuales
Ver [ROADMAP.md](ROADMAP.md) para el plan completo.

**Fase 0 (Actual)**: Fundación arquitectónica
- Prioridad en estructura base y documentación
- Issues marcados con `phase-0`

**Próxima Fase**: MVP Core con Movistar Perú
- Focus en funcionalidad básica
- Issues marcados con `phase-1`

### Cómo Contribuir por Fase

#### Desarrolladores Backend
- Domain entities y business logic
- Adaptadores para diferentes databases
- GraphQL resolvers dinámicos

#### Desarrolladores Frontend  
- Componentes React reutilizables
- Sistema de cross-filtering
- Visualizaciones con Recharts

#### DevOps/Infrastructure
- Docker y K8s configurations
- CI/CD pipelines
- Monitoring y observability

#### Documentación
- API documentation
- Tutorial de setup
- Client onboarding guides

## 🎯 Getting Started - Issues Recomendados

### Para Nuevos Contributors
1. [Setup initial project structure](../../issues/1)
2. [Create Docker development environment](../../issues/2)
3. [Add pre-commit hooks and linting](../../issues/3)

### Para Desarrolladores Experienced
1. [Implement domain entities](../../issues/4)
2. [Create GraphQL dynamic schema generator](../../issues/5)
3. [Build cross-filtering engine](../../issues/6)

## 💬 Comunicación

### Canales
- **GitHub Issues**: Para bugs, features, y discusión técnica
- **GitHub Discussions**: Para preguntas generales y ideas
- **Pull Requests**: Para code review y feedback

### Respuesta Times
- **Issues**: 24-48 horas para primera respuesta
- **Pull Requests**: 48-72 horas para review inicial
- **Questions**: 24 horas en horario laboral

## 🙏 Reconocimiento

Todos los contributors serán reconocidos en:
- README.md contributors section
- CHANGELOG.md para releases
- Hall of Fame para contributors destacados

¡Gracias por ayudar a hacer Pulso-AI mejor! 🚀
