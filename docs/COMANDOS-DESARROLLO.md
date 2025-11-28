# Comandos de Desarrollo - ISFPP

Este documento contiene todos los comandos útiles para el desarrollo del proyecto.

## 📋 Índice Rápido

- [Inicio Rápido](#inicio-rápido)
- [Backend](#backend)
- [Frontend](#frontend)
- [Base de Datos](#base-de-datos)
- [Docker](#docker)
- [Git](#git)
- [Utilidades](#utilidades)

---

## 🚀 Inicio Rápido

### Levantar todo el proyecto (Backend + Frontend)

```bash
# Desde la raíz del proyecto
pnpm dev
```

Esto levanta:
- **Backend**: `http://localhost:99`
- **Frontend**: `http://localhost:3001` (o siguiente disponible)

---

## 🔧 Backend

### Instalar dependencias

```bash
cd backend
pip3 install -r requirements.txt
```

### Ejecutar backend localmente

```bash
cd backend
python3 app.py
```

El backend estará disponible en: `http://localhost:99`

### Instalar Flask-CORS (si falta)

```bash
pip3 install Flask-CORS==4.0.0
```

### Verificar que Flask-CORS está instalado

```bash
python3 -c "from flask_cors import CORS; print('✅ Flask-CORS instalado')"
```

### Probar endpoints del backend

```bash
# Mesas
curl http://localhost:99/api/mesas/ | python3 -m json.tool

# Sectores
curl http://localhost:99/api/sectores/ | python3 -m json.tool

# Con filtros
curl "http://localhost:99/api/mesas/?sector_id=1&tipo=interior" | python3 -m json.tool
```

### Ver logs del backend

Si está corriendo con `pnpm dev`, los logs aparecen en la terminal.

---

## 💻 Frontend

### Instalar dependencias

```bash
cd web
pnpm install
```

### Ejecutar frontend

```bash
cd web
pnpm dev
```

El frontend estará disponible en: `http://localhost:3000` (siempre en el puerto 3000)

**Nota:** El script automáticamente libera el puerto 3000 si está ocupado antes de levantar Vite.

### Build para producción

```bash
cd web
pnpm build
```

### Linter

```bash
cd web
pnpm lint
```

---

## 🗄️ Base de Datos

### ⚠️ IMPORTANTE: PostgreSQL debe estar corriendo

**PostgreSQL está en Docker.** Necesitas tener Docker corriendo para que funcione.

### Levantar PostgreSQL (Docker)

```bash
# Desde la raíz del proyecto
pnpm run db:start

# O desde el directorio backend
cd backend
docker compose up -d database
```

### Verificar que PostgreSQL está corriendo

```bash
# Ver estado
pnpm run db:status

# O ver contenedores
docker ps | grep postgres
```

### Detener PostgreSQL

```bash
pnpm run db:stop

# O desde backend
cd backend
docker compose stop database
```

### Migraciones (con Flask-Migrate)

```bash
cd backend

# Crear nueva migración
python3 -m flask db migrate -m "Descripción de la migración"

# Aplicar migraciones
python3 -m flask db upgrade

# Ver historial de migraciones
python3 -m flask db history

# Revertir última migración
python3 -m flask db downgrade
```

### Ejecutar migraciones en Docker

```bash
# Ejecutar migración dentro del contenedor
docker compose exec backend python3 -m flask db upgrade

# Crear migración
docker compose exec backend python3 -m flask db migrate -m "Descripción"
```

### Conectarse a PostgreSQL (local)

```bash
psql -h localhost -U postgres -d postgresIng
```

### Conectarse a PostgreSQL (Docker)

```bash
docker compose exec postgresIng psql -U postgres -d postgresIng
```

### Ver tablas en la base de datos

```bash
# Desde psql
\dt

# Ver estructura de una tabla
\d nombre_tabla
```

---

## 🐳 Docker

### Levantar servicios (Backend + PostgreSQL)

```bash
# Levantar en segundo plano
docker compose up -d

# Levantar y ver logs
docker compose up

# Ver logs de un servicio específico
docker compose logs -f backend
docker compose logs -f postgresIng
```

### Detener servicios

```bash
docker compose down
```

### Reconstruir imágenes

```bash
# Reconstruir solo el backend
docker compose build backend

# Reconstruir todo sin cache
docker compose build --no-cache

# Reconstruir y levantar
docker compose up -d --build
```

### Ver estado de contenedores

```bash
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores (incluyendo detenidos)
docker ps -a

# Ver solo contenedores del proyecto
docker ps | grep isfpp
```

### Ejecutar comandos dentro del contenedor

```bash
# Ejecutar comando en el backend
docker compose exec backend python3 app.py

# Ejecutar shell en el backend
docker compose exec backend sh

# Instalar paquete en el backend
docker compose exec backend pip install nombre-paquete
```

### Limpiar Docker

```bash
# Detener y eliminar contenedores
docker compose down

# Eliminar también volúmenes (⚠️ CUIDADO: elimina datos)
docker compose down -v

# Limpiar imágenes no usadas
docker system prune -a
```

---

## 🔀 Git

### Ver estado

```bash
git status
```

### Agregar cambios

```bash
# Agregar todos los archivos modificados
git add .

# Agregar archivo específico
git add path/to/file
```

### Commit

```bash
git commit -m "Descripción del cambio"
```

### Ver ramas

```bash
# Ver ramas locales
git branch

# Ver todas las ramas (locales y remotas)
git branch -a
```

### Cambiar de rama

```bash
git checkout nombre-rama

# O crear nueva rama y cambiar
git checkout -b nueva-rama
```

### Merge

```bash
# Desde la rama destino (ej: main)
git checkout main
git merge desarrollo
```

### Push

```bash
# Push de la rama actual
git push

# Push a rama específica
git push origin nombre-rama
```

---

## 🛠️ Utilidades

### Verificar puertos en uso

```bash
# Ver qué está usando el puerto 99
lsof -i :99

# Ver qué está usando el puerto 3000
lsof -i :3000

# Ver todos los puertos en uso
lsof -i -P -n | grep LISTEN
```

### Matar proceso en un puerto

```bash
# Encontrar el PID
lsof -ti :3000

# Matar el proceso
kill -9 $(lsof -ti :3000)

# O usar el script automático (desde la raíz del proyecto)
pnpm run kill:3000
```

**Nota:** El script `dev` automáticamente libera el puerto 3000 antes de levantar el frontend.

### Verificar conexión a la base de datos

```bash
# Desde Python
python3 -c "from backend.db import engine; print('✅ Conectado' if engine.connect() else '❌ Error')"
```

### Verificar que el backend responde

```bash
# Health check simple
curl http://localhost:99/api/mesas/

# Con formato JSON
curl http://localhost:99/api/mesas/ | python3 -m json.tool
```

### Verificar CORS

```bash
curl -X OPTIONS \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: GET" \
  http://localhost:99/api/mesas/ \
  -v 2>&1 | grep -i "access-control"
```

### Buscar archivos

```bash
# Buscar archivo por nombre
find . -name "nombre-archivo.js"

# Buscar texto en archivos
grep -r "texto-buscar" web/src/

# Buscar con regex
grep -r "pattern" --include="*.js" web/src/
```

### Limpiar cache

```bash
# Limpiar cache de Vite
cd web
rm -rf node_modules/.vite

# Limpiar node_modules (si es necesario)
rm -rf node_modules
pnpm install
```

### Ver variables de entorno

```bash
# Ver todas las variables
env

# Ver variable específica
echo $DATABASE_URL
```

---

## 📊 Monitoreo

### Ver logs en tiempo real

```bash
# Logs de Docker
docker compose logs -f

# Logs solo del backend
docker compose logs -f backend

# Últimas 50 líneas
docker compose logs --tail=50 backend
```

### Ver uso de recursos (Docker)

```bash
# Estadísticas de contenedores
docker stats

# Estadísticas de un contenedor específico
docker stats isfpp-backend
```

---

## 🔍 Debugging

### Verificar que Flask-CORS está funcionando

```bash
# Probar petición OPTIONS (preflight)
curl -X OPTIONS \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  http://localhost:99/api/mesas/ \
  -v
```

### Ver errores del backend

Si el backend está corriendo con `pnpm dev`, los errores aparecen en la consola.

Para ver errores en Docker:
```bash
docker compose logs backend | grep -i error
```

### Ver errores del frontend

Abre la consola del navegador (F12) y revisa:
- **Console**: Errores de JavaScript
- **Network**: Peticiones HTTP y sus respuestas

---

## 📊 Métricas de Código

### Ejecutar reporte de métricas

El proyecto cuenta con un script automático para generar métricas de código (Líneas de código, comentarios, complejidad, etc.) tanto para Backend (Python/Radon) como Frontend (React/Sloc).

**Requisitos previos:**
- Tener `pip` instalado (Python).
- Tener `npx` instalado (Node.js).

```bash
# Desde la raíz del proyecto
pip install radon
python3 metrics_runner.py
```

Esto generará una carpeta `metrics/` con:
- `REPORTE_FINAL.txt`: Resumen ejecutivo.
- Archivos `.txt` con el detalle técnico de cada herramienta.

---

## 📝 Notas Importantes

1. **Puertos por defecto:**
   - Backend local: `99`
   - Backend Docker: `8099`
   - Frontend: `3000` (siempre, se libera automáticamente si está ocupado)
   - PostgreSQL: `5432`

2. **Puerto 3000:**
   - El frontend siempre se levanta en el puerto 3000
   - Si el puerto está ocupado, el script automáticamente lo libera antes de levantar Vite
   - Configurado con `strictPort: true` en `vite.config.js` para forzar el uso del puerto 3000

2. **Backend URL en Frontend:**
   - Por defecto: `http://localhost:99`
   - Configurable con variable de entorno: `VITE_BACKEND_URL`

3. **CORS:**
   - Debe estar configurado en `backend/app.py`
   - Flask-CORS debe estar instalado

4. **Base de datos:**
   - Usar migraciones para cambios en el esquema
   - No modificar directamente la base de datos

---

**Última actualización:** Noviembre 2025

