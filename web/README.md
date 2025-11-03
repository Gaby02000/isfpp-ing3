# React - Mejores Prácticas y Librerías Recomendadas

## 🚀 Inicio Rápido

### Desarrollo Local
```bash
npm install
npm run dev
```

### Docker
```bash
docker-compose up web
```

## 📚 Librerías de Estilos Recomendadas

### 1. **Tailwind CSS** (Recomendado)
- **Ventajas**: Utilidades CSS, diseño rápido, altamente personalizable
- **Instalación**: `npm install -D tailwindcss postcss autoprefixer`
- **Ideal para**: Proyectos modernos que requieren diseño flexible y rápido

### 2. **Material-UI (MUI)**
- **Ventajas**: Componentes robustos, sistema de temas, amplia documentación
- **Instalación**: `npm install @mui/material @emotion/react @emotion/styled`
- **Ideal para**: Aplicaciones empresariales que necesitan componentes complejos

### 3. **Chakra UI**
- **Ventajas**: Accesibilidad integrada, diseño simple, buena experiencia de desarrollo
- **Instalación**: `npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion`
- **Ideal para**: Proyectos que priorizan accesibilidad y simplicidad

### 4. **React Bootstrap** (Ya incluido en el proyecto)
- **Ventajas**: Familiar para desarrolladores que conocen Bootstrap
- **Instalación**: Ya incluido `npm install react-bootstrap bootstrap`
- **Ideal para**: Prototipos rápidos y proyectos que ya usan Bootstrap

### 5. **Styled Components**
- **Ventajas**: CSS-in-JS, componentes estilizados, temas dinámicos
- **Instalación**: `npm install styled-components`
- **Ideal para**: Componentes reutilizables con estilos específicos

### 6. **CSS Modules**
- **Ventajas**: Scoped CSS, sin dependencias adicionales, fácil de usar
- **Uso**: Crear archivos `.module.css` junto a tus componentes
- **Ideal para**: Proyectos que prefieren CSS tradicional con scope

## 🎯 Buenas Prácticas de React

### Estructura de Carpetas
```
src/
├── components/          # Componentes reutilizables
│   ├── common/         # Componentes genéricos (Button, Input, etc.)
│   ├── layout/         # Componentes de layout (Header, Footer, etc.)
│   └── [feature]/      # Componentes específicos de una funcionalidad
├── pages/              # Páginas/Views principales
├── hooks/              # Custom hooks
├── services/           # Servicios API
├── utils/              # Utilidades y helpers
├── context/            # Context API
├── store/              # Estado global (Redux, Zustand, etc.)
└── assets/             # Imágenes, fuentes, etc.
```

### Componentes

#### 1. **Nombres Descriptivos**
```jsx
// ❌ Mal
const Comp = () => { ... }

// ✅ Bien
const UserProfileCard = () => { ... }
```

#### 2. **Componentes Pequeños y Enfocados**
```jsx
// ❌ Mal - Componente grande con múltiples responsabilidades
const UserDashboard = () => {
  // 200+ líneas de código
}

// ✅ Bien - Componentes pequeños y específicos
const UserProfile = () => { ... }
const UserStats = () => { ... }
const UserActions = () => { ... }
```

#### 3. **Props Destructuring**
```jsx
// ❌ Mal
const UserCard = (props) => {
  return <div>{props.name}</div>
}

// ✅ Bien
const UserCard = ({ name, email, avatar }) => {
  return <div>{name}</div>
}
```

#### 4. **PropTypes o TypeScript**
```jsx
// Con PropTypes
import PropTypes from 'prop-types'

const UserCard = ({ name, email }) => {
  return <div>{name}</div>
}

UserCard.propTypes = {
  name: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired
}

// Con TypeScript (mejor)
interface UserCardProps {
  name: string
  email: string
}
```

### Hooks

#### 1. **Custom Hooks para Lógica Reutilizable**
```jsx
// hooks/useFetch.js
const useFetch = (url) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [url])

  return { data, loading, error }
}
```

#### 2. **Reglas de Hooks**
```jsx
// ❌ Mal - Llamar hooks condicionalmente
if (condition) {
  const [state, setState] = useState()
}

// ✅ Bien - Siempre llamar hooks al inicio del componente
const [state, setState] = useState()
if (condition) {
  // usar state
}
```

### Estado y Gestión de Datos

#### 1. **useState para Estado Local Simple**
```jsx
const [count, setCount] = useState(0)
```

#### 2. **useReducer para Estado Complejo**
```jsx
const initialState = { count: 0, step: 1 }

const reducer = (state, action) => {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step }
    case 'setStep':
      return { ...state, step: action.payload }
    default:
      return state
  }
}

const [state, dispatch] = useReducer(reducer, initialState)
```

#### 3. **Context API para Estado Global Simple**
```jsx
// context/UserContext.js
const UserContext = createContext()

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  )
}

// Para estado más complejo, usar Zustand o Redux Toolkit
```

### Performance

#### 1. **React.memo para Componentes Costosos**
```jsx
const ExpensiveComponent = React.memo(({ data }) => {
  // Componente que solo se re-renderiza si data cambia
  return <div>{data}</div>
})
```

#### 2. **useMemo para Cálculos Costosos**
```jsx
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b)
}, [a, b])
```

#### 3. **useCallback para Funciones Estables**
```jsx
const handleClick = useCallback(() => {
  doSomething(a, b)
}, [a, b])
```

#### 4. **Lazy Loading de Componentes**
```jsx
import { lazy, Suspense } from 'react'

const LazyComponent = lazy(() => import('./LazyComponent'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  )
}
```

### Manejo de Errores

#### 1. **Error Boundaries**
```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return <h1>Algo salió mal.</h1>
    }
    return this.props.children
  }
}
```

### Formularios

#### 1. **React Hook Form** (Recomendado)
```bash
npm install react-hook-form
```
- Alto rendimiento, validación integrada, menos re-renders

#### 2. **Formik** (Ya incluido en el proyecto)
- Buena para formularios complejos con validación con Yup

### Testing

#### 1. **Vitest** (Recomendado para Vite)
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

#### 2. **Testing Library**
- Siempre prueba desde la perspectiva del usuario
- Usa queries accesibles (getByRole, getByLabelText, etc.)

### Accesibilidad (a11y)

#### 1. **Semántica HTML Correcta**
```jsx
// ❌ Mal
<div onClick={handleClick}>Click me</div>

// ✅ Bien
<button onClick={handleClick}>Click me</button>
```

#### 2. **Atributos ARIA**
```jsx
<button aria-label="Cerrar ventana" onClick={handleClose}>
  <span aria-hidden="true">×</span>
</button>
```

#### 3. **Navegación por Teclado**
- Asegurar que todos los elementos interactivos sean accesibles por teclado
- Usar `tabIndex` apropiadamente

### Código Limpio

#### 1. **Evitar Anidación Profunda**
```jsx
// ❌ Mal
{users.map(user => (
  user.posts.map(post => (
    post.comments.map(comment => (
      <div>{comment.text}</div>
    ))
  ))
))}

// ✅ Bien - Extraer a componentes
{users.map(user => (
  <UserPosts key={user.id} posts={user.posts} />
))}
```

#### 2. **Early Returns**
```jsx
// ❌ Mal
const Component = ({ user }) => {
  if (user) {
    return <div>{user.name}</div>
  } else {
    return null
  }
}

// ✅ Bien
const Component = ({ user }) => {
  if (!user) return null
  return <div>{user.name}</div>
}
```

#### 3. **Separar Lógica de Presentación**
```jsx
// ✅ Bien - Lógica separada
const useUserData = (userId) => {
  const [user, setUser] = useState(null)
  // lógica de fetching
  return { user, loading, error }
}

const UserProfile = ({ userId }) => {
  const { user, loading, error } = useUserData(userId)
  // solo presentación
  if (loading) return <Spinner />
  if (error) return <Error />
  return <div>{user.name}</div>
}
```

## 🔧 Configuración Recomendada

### ESLint
Ya configurado en el proyecto. Asegúrate de seguir las reglas:
```bash
npm run lint
```

### Prettier (Recomendado)
```bash
npm install -D prettier
```

Crear `.prettierrc`:
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

## 📦 Librerías Útiles Adicionales

### Gestión de Estado
- **Zustand**: Estado global simple y ligero
- **Redux Toolkit**: Para aplicaciones complejas
- **Jotai**: Estado atómico, muy moderno

### Routing
- **React Router DOM**: Ya incluido ✅

### Formularios
- **React Hook Form**: Alto rendimiento
- **Formik + Yup**: Ya incluido ✅

### HTTP Client
- **Axios**: Ya incluido ✅
- **SWR**: Para fetching con caché automático
- **React Query (TanStack Query)**: Gestión avanzada de estado del servidor

### Validación
- **Yup**: Ya incluido ✅
- **Zod**: Alternativa moderna con TypeScript

### Utilidades
- **date-fns**: Manipulación de fechas
- **lodash**: Utilidades (usar con moderación)
- **clsx**: Para manejar clases CSS condicionales

## 🎨 Consejos de Diseño

1. **Sistema de Diseño Consistente**
   - Define colores, tipografías y espaciados en un archivo de configuración
   - Usa variables CSS o un objeto de tema

2. **Componentes Reutilizables**
   - Crea una biblioteca de componentes base
   - Documenta con Storybook si es necesario

3. **Responsive Design**
   - Mobile-first approach
   - Usa breakpoints consistentes

4. **Dark Mode**
   - Considera implementar desde el inicio
   - Usa variables CSS para facilitar el cambio

## 📝 Checklist de Desarrollo

- [ ] Componentes pequeños y enfocados
- [ ] Props tipadas (TypeScript o PropTypes)
- [ ] Manejo de errores implementado
- [ ] Loading states para operaciones asíncronas
- [ ] Validación de formularios
- [ ] Accesibilidad básica (semántica, ARIA, teclado)
- [ ] Optimización de performance (memo, useMemo, useCallback cuando sea necesario)
- [ ] Código limpio y legible
- [ ] Tests básicos para lógica crítica
- [ ] Documentación de componentes complejos

## 🔗 Recursos

- [React Official Docs](https://react.dev/)
- [React Patterns](https://reactpatterns.com/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Web.dev - React Performance](https://web.dev/react/)

