# Guía de Migraciones de Base de Datos

Este documento explica cómo usar Flask-Migrate para gestionar las migraciones de la base de datos.

## Configuración

La aplicación está configurada con Flask-Migrate y Flask-SQLAlchemy para gestionar las migraciones de forma profesional.

## Comandos de Migración

### Inicializar el directorio de migraciones (solo la primera vez)

```bash
cd backend
export FLASK_APP=app.py
flask db init
```

O usando el script de pnpm:

```bash
cd backend
pnpm run db:init
```

Esto creará el directorio `migrations/` con la estructura necesaria.

### Crear una nueva migración

Cuando modifiques los modelos (en `models/`), crea una nueva migración:

```bash
export FLASK_APP=app.py
flask db migrate -m "Descripción de los cambios"
```

O usando el script de pnpm:

```bash
pnpm run db:migrate "Descripción de los cambios"
```

**Ejemplo:**
```bash
pnpm run db:migrate "Agregar campo email a tabla Usuario"
```

### Aplicar migraciones

Para aplicar las migraciones pendientes a la base de datos:

```bash
export FLASK_APP=app.py
flask db upgrade
```

O usando el script de pnpm:

```bash
pnpm run db:upgrade
```

### Revertir la última migración

Si necesitas revertir la última migración aplicada:

```bash
export FLASK_APP=app.py
flask db downgrade
```

O usando el script de pnpm:

```bash
pnpm run db:downgrade
```

### Ver el historial de migraciones

```bash
export FLASK_APP=app.py
flask db history
```

O usando el script de pnpm:

```bash
pnpm run db:history
```

### Ver la migración actual

```bash
export FLASK_APP=app.py
flask db current
```

O usando el script de pnpm:

```bash
pnpm run db:current
```

## Flujo de Trabajo Recomendado

1. **Modificar los modelos** en `models/` (ej: agregar un campo, crear una tabla)
2. **Crear la migración:**
   ```bash
   pnpm run db:migrate "Descripción del cambio"
   ```
3. **Revisar el archivo de migración** generado en `migrations/versions/`
4. **Aplicar la migración:**
   ```bash
   pnpm run db:upgrade
   ```

## Variables de Entorno

Para que Flask-Migrate funcione correctamente, asegúrate de tener configurada la variable de entorno:

```bash
export FLASK_APP=app.py
export DATABASE_URL=postgresql://postgres:postgres@database/postgresIng
```

O crear un archivo `.env` en `backend/`:

```
FLASK_APP=app.py
DATABASE_URL=postgresql://postgres:postgres@database/postgresIng
```

## Notas Importantes

- **En desarrollo**: Las tablas se crean automáticamente usando `Base.metadata.create_all()` si `FLASK_ENV != 'production'`
- **En producción**: Siempre usar migraciones (`flask db upgrade`) antes de iniciar la aplicación
- **Nunca editar manualmente** los archivos de migración una vez creados (a menos que sepas lo que estás haciendo)
- **Siempre revisar** el archivo de migración generado antes de aplicarlo
- **Backup**: Hacer backup de la base de datos antes de aplicar migraciones en producción

## Estructura de Directorios

```
backend/
├── migrations/          # Directorio de migraciones (generado por flask db init)
│   ├── versions/       # Archivos de migración individuales
│   ├── env.py          # Configuración del entorno de migraciones
│   └── script.py.mako  # Plantilla para migraciones
├── models/             # Modelos SQLAlchemy
├── app.py              # Aplicación Flask con configuración de migraciones
└── db.py               # Configuración de base de datos
```

