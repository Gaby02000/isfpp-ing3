# Seeders - Datos de Prueba

Esta carpeta contiene los seeders (cargadores de datos falsos) organizados por entidad.

## Estructura

```
seed/
├── __init__.py              # Exporta la función main
├── insert_seed.py           # Script principal que ejecuta todos los seeders
├── sector/
│   ├── __init__.py
│   └── seed_sector.py       # Seeder para Sectores
├── seccion/
│   ├── __init__.py
│   └── seed_seccion.py      # Seeder para Secciones de Carta
├── producto/
│   ├── __init__.py
│   └── seed_producto.py     # Seeder para Productos (Platos, Postres, Bebidas)
└── mesa/
    ├── __init__.py
    └── seed_mesa.py         # Seeder para Mesas
```

## Uso

### Ejecutar todos los seeders
```bash
pnpm seed
```

O directamente:
```bash
python3 -m seed.insert_seed
```

### Agregar un nuevo seeder

1. Crear una nueva carpeta dentro de `seed/` con el nombre de la entidad
2. Crear `__init__.py` que exporte la función seeder
3. Crear `seed_<entidad>.py` con la función `seed_<entidad>(session, ...)`
4. Importar y llamar la función en `insert_seed.py`

**Ejemplo:**
```python
# seed/cliente/__init__.py
from .seed_cliente import seed_clientes
__all__ = ['seed_clientes']

# seed/cliente/seed_cliente.py
from models import Cliente

def seed_clientes(session):
    # Lógica del seeder
    pass

# seed/insert_seed.py
from seed.cliente.seed_cliente import seed_clientes
# ... en main():
clientes = seed_clientes(session)
```

## Datos Generados

El seeder actual genera:
- **5 Sectores** (números 1-5)
- **5 Secciones de Carta** (Entradas, Platos Principales, Postres, Bebidas, Menú del Día)
- **16 Productos** (3 entradas, 5 platos principales, 4 postres, 4 bebidas, 1 menú del día)
- **20-30 Mesas** (4-6 mesas por sector, distribuidas aleatoriamente)

## Notas

- El seeder **limpia los datos existentes** antes de crear nuevos datos
- Las dependencias se respetan en el orden de ejecución:
  1. Sectores (sin dependencias)
  2. Secciones (sin dependencias)
  3. Productos (depende de Secciones)
  4. Mesas (depende de Sectores)

