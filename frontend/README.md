# ⚛️ Frontend Pulso-AI

Aplicación React con **GraphQL** y **cross-filtering inteligente** para dashboards multi-cliente.

## 🎯 Arquitectura Frontend

```
frontend/
├── public/                  # Assets estáticos
├── src/
│   ├── components/         # Componentes React reutilizables
│   │   ├── common/        # Componentes base (Button, Input, etc.)
│   │   ├── dashboard/     # Componentes específicos de dashboard
│   │   ├── filters/       # Sistema de cross-filtering
│   │   └── charts/        # Visualizaciones con Recharts
│   ├── hooks/             # Custom hooks de React
│   │   ├── useFilters.ts  # Hook para cross-filtering
│   │   ├── useDashboard.ts # Hook para dashboard state
│   │   └── useClient.ts   # Hook para contexto de cliente
│   ├── graphql/           # GraphQL queries y mutations
│   │   ├── queries/       # Queries organizadas por dominio
│   │   ├── mutations/     # Mutations para updates
│   │   ├── fragments/     # Fragmentos reutilizables
│   │   └── generated/     # Tipos TypeScript autogenerados
│   ├── utils/             # Utilidades y helpers
│   │   ├── formatting.ts  # Formateo de datos
│   │   ├── validation.ts  # Validaciones frontend
│   │   └── constants.ts   # Constantes de la aplicación
│   ├── types/             # Definiciones TypeScript
│   ├── context/           # Context providers de React
│   └── pages/             # Páginas principales (si usando routing)
├── package.json           # Dependencies y scripts
├── vite.config.ts         # Configuración Vite
├── tailwind.config.js     # Configuración Tailwind CSS
├── tsconfig.json          # Configuración TypeScript
└── README.md              # Este archivo
```

## 🛠️ Stack Tecnológico

### Core Framework
- **React 18**: UI framework con Concurrent Features
- **TypeScript**: Type safety y mejor DX
- **Vite**: Build tool ultra-rápido

### Estado y Data Fetching  
- **Apollo Client**: GraphQL client con cache inteligente
- **React Query** (opcional): Para queries REST si necesario
- **Zustand**: State management ligero para estado global

### Styling y UI
- **Tailwind CSS**: Utility-first CSS framework
- **Headless UI**: Componentes accesibles sin styling
- **Recharts**: Gráficos responsivos y customizables

### Developer Experience
- **ESLint + Prettier**: Linting y formateo
- **Husky**: Git hooks para calidad de código
- **Storybook**: Documentación de componentes
- **Vitest**: Testing ultra-rápido

## 🎨 Sistema de Diseño

### Principios
1. **Mobile First**: Responsive design por defecto
2. **Accessibility**: WCAG 2.1 compliance
3. **Performance**: Componentes lazy-loaded
4. **Consistency**: Design tokens centralizados

### Tema Base
```typescript
// src/theme/tokens.ts
export const theme = {
  colors: {
    primary: '#3B82F6',    // Azul principal
    secondary: '#10B981',  // Verde éxito  
    warning: '#F59E0B',    // Amarillo warning
    error: '#EF4444',      // Rojo error
    gray: {
      50: '#F9FAFB',
      900: '#111827'
    }
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem', 
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem'
  }
}
```

## 🔄 Cross-Filtering Architecture

### Concepto
El **cross-filtering** permite que los filtros se actualicen dinámicamente basándose en las selecciones del usuario.

```typescript
// Ejemplo de cross-filtering flow
Usuario selecciona "Ejecutivo: Juan Pérez"
  ↓
Hook useFilters detecta cambio
  ↓  
GraphQL query con nuevos filtros
  ↓
Backend retorna valores válidos para otras dimensiones
  ↓
UI actualiza opciones disponibles automáticamente
```

### Implementación
```typescript
// hooks/useFilters.ts
export function useFilters() {
  const [filters, setFilters] = useState<FilterState[]>([]);
  
  const { data: availableFilters } = useQuery(
    GET_AVAILABLE_FILTERS,
    { variables: { currentFilters: filters } }
  );
  
  return {
    filters,
    setFilters,
    availableFilters: availableFilters?.suggestions || []
  };
}
```

## 📊 Componentes Dashboard

### DashboardContainer
Componente principal que orchestrates toda la experiencia de dashboard.

### FilterPanel  
Panel lateral con todos los filtros cross-filtering.

### VisualizationGrid
Grid responsivo que muestra gráficos y tablas.

### MetricsCards
Cards con métricas clave y sparklines.

## 🎯 Multi-Client Support

### Client Context
```typescript
// context/ClientContext.tsx
export const ClientContext = createContext<{
  clientId: string;
  clientConfig: ClientConfig;
  dimensions: Dimension[];
  metrics: Metric[];
}>({});
```

### Dynamic Schema
El frontend se adapta automáticamente al schema GraphQL generado dinámicamente por cada cliente.

### Customization
- **Branding**: Logo y colores por cliente
- **Dimensions**: Filtros específicos por cliente  
- **Metrics**: KPIs customizados
- **Layout**: Disposición de componentes

## 🚀 Development Workflow

### Setup Local
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint

# Testing
npm run test
```

### Feature Development
```bash
# 1. Create component
src/components/NewComponent/

# 2. Add to Storybook
src/components/NewComponent/NewComponent.stories.tsx

# 3. Write tests
src/components/NewComponent/NewComponent.test.tsx

# 4. Document in README
```

## 📱 Responsive Design

### Breakpoints
```css
/* Tailwind breakpoints */
sm: 640px   /* Tablet */
md: 768px   /* Desktop small */
lg: 1024px  /* Desktop */
xl: 1280px  /* Desktop large */
2xl: 1536px /* Desktop XL */
```

### Dashboard Layout
- **Mobile**: Single column, collapsible filters
- **Tablet**: Two columns, sidebar filters
- **Desktop**: Multi-column grid, persistent sidebar

## 🔐 Security

### Authentication
- JWT tokens almacenados en httpOnly cookies
- Auto-refresh de tokens
- Logout automático en expiración

### Client Isolation
- **Route-based**: `/client/:clientId/dashboard`
- **Context-aware**: Componentes saben su cliente actual
- **Data validation**: Verificación client-side de permisos

## 📈 Performance

### Optimizations
- **Code Splitting**: Lazy loading por rutas
- **Bundle Analysis**: Webpack Bundle Analyzer
- **Image Optimization**: Responsive images con lazy loading
- **GraphQL**: Query deduplication y cache

### Metrics
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s  
- **Bundle Size**: < 500KB gzipped

---

**Next Steps**: Configurar proyecto Vite con TypeScript y instalar dependencias base.
