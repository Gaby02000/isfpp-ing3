# Buenas Prácticas para React y Flask

Este documento contiene buenas prácticas y recomendaciones para desarrollar aplicaciones web con React (frontend) y Flask (backend).

## 📋 Tabla de Contenidos

- [React - Buenas Prácticas](#react---buenas-prácticas)
- [Flask - Buenas Prácticas](#flask---buenas-prácticas)
- [Arquitectura y Estructura](#arquitectura-y-estructura)
- [Seguridad](#seguridad)
- [Testing](#testing)
- [Performance](#performance)

---

## React - Buenas Prácticas

### 1. Estructura de Carpetas

```
src/
├── components/          # Componentes reutilizables
│   ├── common/         # Componentes genéricos (Cargador, MensajeAlerta, etc.)
│   ├── layout/         # Componentes de layout (Plantilla, BarraNavegacion)
│   └── [feature]/      # Componentes específicos de una funcionalidad
├── pages/              # Páginas/Vistas principales
├── hooks/              # Custom hooks personalizados
├── services/           # Servicios API y comunicación con backend
├── utils/              # Utilidades y helpers
├── constants/          # Constantes de la aplicación
├── context/            # Context API para estado global
└── assets/             # Imágenes, fuentes, estilos
```

### 2. Nomenclatura de Componentes

**✅ Correcto:**
- Nombres en español y descriptivos
- PascalCase para componentes
- Nombres que indiquen claramente su propósito

```jsx
// Componentes en español
const Cargador = () => { ... }
const MensajeAlerta = () => { ... }
const CampoFormulario = () => { ... }
const BarraNavegacion = () => { ... }
```

**❌ Incorrecto:**
```jsx
// Nombres genéricos o en inglés
const Comp = () => { ... }
const LoadingSpinner = () => { ... }
const Alert = () => { ... }
```

### 3. Componentes Pequeños y Enfocados

**✅ Correcto:**
```jsx
// Componente pequeño y enfocado en una responsabilidad
const CampoFormulario = ({ label, name, value, onChange, error }) => {
  return (
    <Form.Group className="mb-3">
      <Form.Label>{label}</Form.Label>
      <Form.Control
        name={name}
        value={value}
        onChange={onChange}
        isInvalid={error}
      />
      {error && <Form.Control.Feedback type="invalid">{error}</Form.Control.Feedback>}
    </Form.Group>
  );
};
```

**❌ Incorrecto:**
```jsx
// Componente grande con múltiples responsabilidades
const FormularioCompleto = () => {
  // 200+ líneas de código mezclando lógica y presentación
};
```

### 4. Custom Hooks para Lógica Reutilizable

**✅ Correcto:**
```jsx
// hooks/useMozoService.js
export const useMozoService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const createMozo = useCallback(async (mozoData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${BACKEND_URL}/mozos`, mozoData);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al crear el mozo');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createMozo, error, loading };
};
```

### 5. Validación con Yup

**✅ Correcto:**
```jsx
// utils/validations.js
import * as Yup from 'yup';

export const mozoValidationSchema = Yup.object({
  dni: Yup.string()
    .required('El DNI es requerido')
    .matches(/^\d+$/, 'El DNI debe contener solo números'),
  nombre: Yup.string()
    .required('El nombre es requerido')
    .min(2, 'El nombre debe tener al menos 2 caracteres'),
  telefono: Yup.string()
    .required('El teléfono es requerido')
    .matches(/^\d+$/, 'El teléfono debe contener solo números'),
});
```

### 6. Manejo de Estado

#### Estado Local Simple - useState
```jsx
const [nombre, setNombre] = useState('');
const [loading, setLoading] = useState(false);
```

#### Estado Complejo - useReducer
```jsx
const initialState = { count: 0, step: 1 };

const reducer = (state, action) => {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'setStep':
      return { ...state, step: action.payload };
    default:
      return state;
  }
};

const [state, dispatch] = useReducer(reducer, initialState);
```

#### Estado Global - Context API
```jsx
// context/UsuarioContext.js
const UsuarioContext = createContext();

export const UsuarioProvider = ({ children }) => {
  const [usuario, setUsuario] = useState(null);
  
  return (
    <UsuarioContext.Provider value={{ usuario, setUsuario }}>
      {children}
    </UsuarioContext.Provider>
  );
};
```

### 7. Performance

#### React.memo para Componentes Costosos
```jsx
const ComponenteCostoso = React.memo(({ data }) => {
  // Solo se re-renderiza si data cambia
  return <div>{data}</div>;
});
```

#### useMemo para Cálculos Costosos
```jsx
const resultadoCostoso = useMemo(() => {
  return calcularResultado(a, b);
}, [a, b]);
```

#### useCallback para Funciones Estables
```jsx
const handleClick = useCallback(() => {
  hacerAlgo(a, b);
}, [a, b]);
```

#### Lazy Loading de Componentes
```jsx
import { lazy, Suspense } from 'react';

const ComponenteLazy = lazy(() => import('./ComponenteLazy'));

function App() {
  return (
    <Suspense fallback={<Cargador />}>
      <ComponenteLazy />
    </Suspense>
  );
}
```

### 8. Manejo de Errores

#### Error Boundaries
```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error:', error, errorInfo);
    // Enviar error a servicio de logging
  }

  render() {
    if (this.state.hasError) {
      return <MensajeAlerta variant="danger" message="Algo salió mal" />;
    }
    return this.props.children;
  }
}
```

### 9. Formularios

#### Usando Formik + Yup
```jsx
<Formik
  initialValues={{ nombre: '', email: '' }}
  validationSchema={validationSchema}
  onSubmit={async (values, { setSubmitting, setStatus }) => {
    try {
      await crearUsuario(values);
      setStatus({ success: 'Usuario creado exitosamente' });
    } catch (error) {
      setStatus({ error: error.message });
    } finally {
      setSubmitting(false);
    }
  }}
>
  {({ handleSubmit, isSubmitting, status }) => (
    <Form onSubmit={handleSubmit}>
      {/* Campos del formulario */}
    </Form>
  )}
</Formik>
```

### 10. Accesibilidad (a11y)

```jsx
// ✅ Correcto - Semántica HTML y ARIA
<button 
  aria-label="Cerrar ventana" 
  onClick={handleClose}
>
  <span aria-hidden="true">×</span>
</button>

// ✅ Correcto - Navegación por teclado
<div 
  role="button"
  tabIndex={0}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  onClick={handleClick}
>
  Hacer clic
</div>
```

---

## Flask - Buenas Prácticas

### 1. Estructura de Carpetas

```
backend/
├── app.py              # Punto de entrada de la aplicación
├── db.py               # Configuración de base de datos
├── models/             # Modelos SQLAlchemy
│   ├── __init__.py
│   └── models.py
├── routes/             # Blueprints y rutas
│   ├── __init__.py
│   ├── producto_routes.py
│   └── seccion_routes.py
├── services/           # Lógica de negocio
├── utils/              # Utilidades y helpers
├── config.py           # Configuración de la aplicación
└── requirements.txt    # Dependencias
```

### 2. Blueprints para Organizar Rutas

**✅ Correcto:**
```python
# routes/producto_routes.py
from flask import Blueprint, jsonify, request
from db import SessionLocal
from models.models import Producto

producto_bp = Blueprint('producto', __name__)

@producto_bp.route('/', methods=['GET'])
def listar_productos():
    session = SessionLocal()
    try:
        productos = session.query(Producto).filter_by(baja=False).all()
        return jsonify({
            'status': 'success',
            'data': [p.json() for p in productos]
        }), 200
    finally:
        session.close()
```

**✅ Registro en app.py:**
```python
from routes import producto_bp

app.register_blueprint(producto_bp, url_prefix='/api/productos')
```

### 3. Manejo de Sesiones de Base de Datos

**✅ Correcto - Usar try/finally:**
```python
@producto_bp.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    session = SessionLocal()
    try:
        producto = session.query(Producto).get(id)
        if not producto:
            return jsonify({
                'status': 'error',
                'message': 'Producto no encontrado'
            }), 404
        return jsonify({
            'status': 'success',
            'data': producto.json()
        }), 200
    finally:
        session.close()
```

**❌ Incorrecto - Olvidar cerrar sesión:**
```python
# ❌ No cerrar la sesión puede causar fugas de memoria
session = SessionLocal()
producto = session.query(Producto).get(id)
return jsonify(producto.json())
```

### 4. Validación de Datos

**✅ Correcto:**
```python
@producto_bp.route('/', methods=['POST'])
def crear_producto():
    session = SessionLocal()
    data = request.get_json()
    
    # Validar campos requeridos
    campos_requeridos = ['codigo', 'nombre', 'precio', 'id_seccion']
    for campo in campos_requeridos:
        if campo not in data:
            session.close()
            return jsonify({
                'status': 'error',
                'message': f'El campo "{campo}" es requerido'
            }), 400
    
    # Validar tipos de datos
    if not isinstance(data['precio'], (int, float)) or data['precio'] <= 0:
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'El precio debe ser un número positivo'
        }), 400
    
    try:
        # Crear producto
        nuevo = Producto(
            codigo=data['codigo'],
            nombre=data['nombre'],
            precio=data['precio'],
            id_seccion=data['id_seccion']
        )
        session.add(nuevo)
        session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Producto creado correctamente',
            'data': nuevo.json()
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        session.close()
```

### 5. Respuestas JSON Consistentes

**✅ Correcto:**
```python
# Estructura consistente de respuestas
def respuesta_exito(data, mensaje=None, codigo=200):
    respuesta = {'status': 'success', 'data': data}
    if mensaje:
        respuesta['message'] = mensaje
    return jsonify(respuesta), codigo

def respuesta_error(mensaje, codigo=400):
    return jsonify({
        'status': 'error',
        'message': mensaje
    }), codigo

# Uso
@producto_bp.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    session = SessionLocal()
    try:
        producto = session.query(Producto).get(id)
        if not producto:
            return respuesta_error('Producto no encontrado', 404)
        return respuesta_exito(producto.json())
    finally:
        session.close()
```

### 6. Manejo de Errores

**✅ Correcto:**
```python
from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Recurso no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Error interno del servidor'
    }), 500

@app.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Error en la base de datos'
    }), 500
```

### 7. Configuración con Variables de Entorno

**✅ Correcto:**
```python
# config.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# app.py
from config import Config

app.config.from_object(Config)
```

### 8. Soft Delete (Baja Lógica)

**✅ Correcto:**
```python
@producto_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    session = SessionLocal()
    try:
        producto = session.query(Producto).get(id)
        if not producto or producto.baja:
            return respuesta_error('Producto no encontrado', 404)
        
        # Soft delete - no eliminar físicamente
        producto.baja = True
        session.commit()
        
        return respuesta_exito(
            producto.json(),
            'Producto dado de baja correctamente'
        )
    except Exception as e:
        session.rollback()
        return respuesta_error(str(e), 500)
    finally:
        session.close()
```

### 9. Serialización de Modelos

**✅ Correcto:**
```python
class Producto(Base):
    __tablename__ = 'producto'
    id_producto = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(255), nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    
    def json(self):
        return {
            'id_producto': self.id_producto,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'precio': float(self.precio),  # Convertir DECIMAL a float
            'baja': self.baja
        }
```

### 10. CORS para Desarrollo

**✅ Correcto:**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Para desarrollo

# Para producción, configurar CORS específicamente:
# CORS(app, resources={r"/api/*": {"origins": "https://tudominio.com"}})
```

---

## Arquitectura y Estructura

### Separación de Responsabilidades

**✅ Correcto:**
- **Routes**: Solo manejan HTTP requests/responses
- **Services**: Lógica de negocio
- **Models**: Estructura de datos
- **Utils**: Funciones auxiliares

```python
# routes/producto_routes.py - Solo HTTP
@producto_bp.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = producto_service.obtener_por_id(id)
    return respuesta_exito(producto.json())

# services/producto_service.py - Lógica de negocio
def obtener_por_id(id):
    session = SessionLocal()
    try:
        producto = session.query(Producto).get(id)
        if not producto:
            raise ValueError('Producto no encontrado')
        return producto
    finally:
        session.close()
```

---

## Seguridad

### 1. Validación de Entrada

**✅ Correcto:**
```python
# Validar y sanitizar datos de entrada
import re

def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitizar_string(texto):
    return texto.strip()[:255]  # Limitar longitud
```

### 2. Manejo de Errores sin Exponer Información

**✅ Correcto:**
```python
# No exponer detalles internos en producción
if app.config['DEBUG']:
    return jsonify({'error': str(e)}), 500
else:
    return jsonify({'error': 'Error interno del servidor'}), 500
```

### 3. SQL Injection Prevention

**✅ Correcto:**
```python
# Usar SQLAlchemy ORM (ya previene SQL injection)
producto = session.query(Producto).filter_by(codigo=codigo).first()

# ❌ Nunca hacer esto:
# session.execute(f"SELECT * FROM producto WHERE codigo = '{codigo}'")
```

---

## Testing

### React Testing

```jsx
// Componente.test.jsx
import { render, screen } from '@testing-library/react';
import { Cargador } from './Cargador';

test('muestra el spinner de carga', () => {
  render(<Cargador />);
  const spinner = screen.getByRole('status');
  expect(spinner).toBeInTheDocument();
});
```

### Flask Testing

```python
# tests/test_producto_routes.py
import unittest
from app import app
from db import SessionLocal
from models.models import Producto

class TestProductoRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_listar_productos(self):
        response = self.app.get('/api/productos/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
```

---

## Performance

### React

1. **Code Splitting**: Usar lazy loading para componentes grandes
2. **Memoización**: React.memo, useMemo, useCallback cuando sea necesario
3. **Virtualización**: Para listas grandes (react-window)
4. **Optimización de imágenes**: Usar formatos modernos (WebP)

### Flask

1. **Conexión a BD**: Usar connection pooling
2. **Caché**: Implementar caché para datos frecuentemente consultados
3. **Paginación**: Para listas grandes
4. **Índices de BD**: Crear índices en columnas frecuentemente consultadas

```python
# Paginación
@producto_bp.route('/', methods=['GET'])
def listar_productos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    session = SessionLocal()
    try:
        productos = session.query(Producto)\
            .filter_by(baja=False)\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'status': 'success',
            'data': [p.json() for p in productos.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': productos.total,
                'pages': productos.pages
            }
        }), 200
    finally:
        session.close()
```

---

## Checklist de Desarrollo

### React
- [ ] Componentes pequeños y enfocados
- [ ] Props tipadas (TypeScript o PropTypes)
- [ ] Manejo de errores implementado
- [ ] Loading states para operaciones asíncronas
- [ ] Validación de formularios
- [ ] Accesibilidad básica (semántica, ARIA, teclado)
- [ ] Optimización de performance (memo, useMemo, useCallback)
- [ ] Código limpio y legible
- [ ] Tests básicos para lógica crítica

### Flask
- [ ] Blueprints para organizar rutas
- [ ] Validación de entrada en todos los endpoints
- [ ] Manejo correcto de sesiones de BD (try/finally)
- [ ] Respuestas JSON consistentes
- [ ] Manejo de errores con try/except
- [ ] Soft delete para datos importantes
- [ ] Variables de entorno para configuración
- [ ] CORS configurado correctamente
- [ ] Tests para endpoints críticos

---

## Recursos Adicionales

### React
- [React Official Docs](https://react.dev/)
- [React Patterns](https://reactpatterns.com/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask Best Practices](https://exploreflask.com/en/latest/)

---

**Última actualización:** 2024

