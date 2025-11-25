# Tests del Backend

Este directorio contiene todos los tests unitarios e de integración para el backend de la aplicación.

## Estructura

```
tests/
├── __init__.py
├── conftest.py                    # Configuración compartida (fixtures, DB de test)
├── test_cliente.py                # Tests para módulo Cliente
├── test_comanda.py                # Tests para módulo Comanda
├── test_mesa.py                   # Tests para módulo Mesa
├── test_mozo.py                   # Tests para módulo Mozo
├── test_producto.py               # Tests para módulo Producto
├── test_seccion.py                # Tests para módulo Seccion
├── test_sector.py                 # Tests para módulo Sector
├── test_medio_pago.py             # Tests para módulo MedioPago
└── utils/
    ├── __init__.py
    └── test_helpers.py            # Funciones auxiliares para tests
```

## Instalación

Primero, instala las dependencias de testing:

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `pytest==7.4.3` - Framework de testing
- `pytest-flask==1.3.0` - Extensiones para Flask
- `pytest-cov==4.1.0` - Cobertura de código
- `faker==20.1.0` - Generación de datos de prueba

## Ejecutar Tests

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests con verbose (más información)

```bash
pytest -v
```

### Ejecutar tests con cobertura

```bash
pytest --cov=. --cov-report=html
```

Esto generará un reporte HTML en `htmlcov/index.html` que puedes abrir en tu navegador.

### Ejecutar un archivo específico

```bash
pytest tests/test_cliente.py
```

### Ejecutar un test específico

```bash
pytest tests/test_cliente.py::TestClienteRoutes::test_crear_cliente_exitoso
```

### Ejecutar tests con salida detallada

```bash
pytest -v -s
```

## Cobertura de Tests

Cada módulo tiene tests que cubren:

### Tests de Modelos (Unitarios)
- ✅ Creación de objetos
- ✅ Validaciones de campos
- ✅ Método `json()`
- ✅ Validación de unicidad
- ✅ Relaciones entre modelos

### Tests de Rutas (Integración)
- ✅ GET / (listar con filtros y paginación)
- ✅ POST / (crear)
- ✅ GET /<id> (obtener)
- ✅ PUT /<id> (modificar)
- ✅ DELETE /<id> (baja lógica)
- ✅ Validaciones de errores (400, 404, 500)
- ✅ Validaciones de negocio (duplicados, estados, etc.)
- ✅ Filtros y búsquedas
- ✅ Paginación
- ✅ Ordenamiento

## Módulos Testeados

1. **Cliente** - Gestión de clientes
2. **Comanda** - Gestión de comandas/pedidos
3. **Mesa** - Gestión de mesas
4. **Mozo** - Gestión de mozos
5. **Producto** - Gestión de productos (Plato, Postre, Bebida)
6. **Seccion** - Categorías de productos
7. **Sector** - Sectores del restaurante
8. **MedioPago** - Medios de pago

## Configuración de Base de Datos de Test

Los tests usan una base de datos SQLite en memoria (`sqlite:///:memory:`) que se crea y destruye automáticamente para cada sesión de tests. Esto garantiza:

- ✅ Tests aislados y rápidos
- ✅ No afecta la base de datos de desarrollo
- ✅ Cada test comienza con un estado limpio

## Fixtures Disponibles

El archivo `conftest.py` proporciona fixtures reutilizables:

- `test_app` - Aplicación Flask configurada para testing
- `test_client` - Cliente HTTP para hacer requests
- `test_db_session` - Sesión de base de datos para cada test
- `sample_*_data` - Datos de ejemplo para crear objetos
- `created_*` - Objetos ya creados en la BD (para tests que requieren relaciones)

## Ejemplos de Uso

### Ejemplo 1: Test simple

```python
def test_crear_cliente_exitoso(test_client, sample_cliente_data):
    response = test_client.post('/api/clientes/', json=sample_cliente_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'
```

### Ejemplo 2: Test con relaciones

```python
def test_crear_comanda(test_client, created_mozo, created_mesa, sample_comanda_data):
    comanda_data = sample_comanda_data.copy()
    comanda_data['id_mozo'] = created_mozo.id
    comanda_data['id_mesa'] = created_mesa.id_mesa
    
    response = test_client.post('/api/comandas/', json=comanda_data)
    assert response.status_code == 201
```

## Notas Importantes

- Los tests usan transacciones que se hacen rollback automáticamente después de cada test
- La base de datos se crea y destruye por sesión, no por test individual
- Los fixtures `created_*` crean objetos en la BD que pueden ser usados por múltiples tests
- Los helpers en `test_helpers.py` proporcionan funciones útiles para validar respuestas

## Troubleshooting

### Error: "No module named 'pytest'"
```bash
pip install -r requirements.txt
```

### Error: "Database locked"
Esto puede ocurrir si hay múltiples procesos ejecutando tests. Asegúrate de cerrar otras instancias.

### Tests fallan con errores de importación
Asegúrate de ejecutar los tests desde el directorio `backend/`:
```bash
cd backend
pytest
```

