# Configuración CORS y Conectividad Frontend-Backend

Este documento explica cómo configurar CORS (Cross-Origin Resource Sharing) para permitir que el frontend se comunique con el backend, y todos los comandos necesarios para el desarrollo.

## 📋 Tabla de Contenidos

1. [Configuración de CORS](#configuración-de-cors)
2. [Instalación de Flask-CORS](#instalación-de-flask-cors)
3. [Configuración del Frontend](#configuración-del-frontend)
4. [Comandos para Levantar el Proyecto](#comandos-para-levantar-el-proyecto)
5. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Configuración de CORS

### ¿Qué es CORS?

CORS (Cross-Origin Resource Sharing) es un mecanismo de seguridad que permite que un navegador permita peticiones desde un origen (dominio) diferente. En nuestro caso, el frontend (React) corre en `http://localhost:3001` y necesita hacer peticiones al backend (Flask) que corre en `http://localhost:99`.

### Configuración en el Backend

El archivo `backend/app.py` debe incluir la configuración de CORS:

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Configurar CORS para permitir peticiones desde el frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:3002",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://127.0.0.1:3002"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## 📦 Instalación de Flask-CORS

### Instalación Local (Entorno Python)

Si estás ejecutando el backend localmente (fuera de Docker):

```bash
# Instalar Flask-CORS en el entorno local
pip3 install Flask-CORS==4.0.0

# Verificar instalación
python3 -c "from flask_cors import CORS; print('✅ Flask-CORS instalado')"
```

### Instalación en Docker

Si estás usando Docker, Flask-CORS debe estar en `requirements.txt`:

```txt
Flask-CORS==4.0.0
```

Luego, reconstruir la imagen:

```bash
# Reconstruir la imagen del backend
docker compose build backend

# Reiniciar el contenedor
docker compose up -d backend
```

O instalar directamente en el contenedor (temporal):

```bash
# Instalar en el contenedor en ejecución
docker compose exec backend pip install Flask-CORS==4.0.0

# Reiniciar el contenedor
docker compose restart backend
```

---

## ⚙️ Configuración del Frontend

### URLs del Backend

Los servicios del frontend (`web/src/services/`) están configurados para conectarse al backend:

**Configuración por defecto:**
- **Backend Local**: `http://localhost:99` (cuando ejecutas `pnpm dev` desde la raíz)
- **Backend Docker**: `http://localhost:8099` (si prefieres usar Docker)

**Archivos configurados:**
- `web/src/services/mesaService.js`
- `web/src/services/sectorService.js`
- `web/src/services/mozoService.js`

**Ejemplo de configuración:**
```javascript
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:99';
```

### Cambiar el Backend URL

Si quieres usar Docker en lugar del backend local:

1. **Opción 1: Variable de entorno**
   ```bash
   # Crear archivo .env en web/
   echo "VITE_BACKEND_URL=http://localhost:8099" > web/.env
   ```

2. **Opción 2: Modificar directamente**
   Cambiar en los archivos de servicios:
   ```javascript
   const BACKEND_URL = 'http://localhost:8099'; // Docker
   // o
   const BACKEND_URL = 'http://localhost:99';   // Local
   ```

---

## 🚀 Comandos para Levantar el Proyecto

### Opción 1: Backend Local + Frontend

**Desde la raíz del proyecto:**
```bash
# Levantar backend y frontend simultáneamente
pnpm dev
```

Esto ejecuta:
- **Backend**: `http://localhost:99` (Flask local)
- **Frontend**: `http://localhost:3001` (o el siguiente puerto disponible)

### Opción 2: Docker (Backend + PostgreSQL)

**Levantar servicios Docker:**
```bash
# Levantar PostgreSQL y Backend en Docker
docker compose up -d

# Ver logs
docker compose logs -f backend

# Detener servicios
docker compose down
```

**Luego levantar solo el frontend:**
```bash
cd web
pnpm dev
```

### Opción 3: Todo Manualmente

**Terminal 1 - Backend:**
```bash
cd backend
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd web
pnpm dev
```

---

## 🔍 Verificación de CORS

### Verificar que CORS está funcionando

**Desde la terminal:**
```bash
# Verificar headers CORS
curl -X OPTIONS \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: GET" \
  http://localhost:99/api/mesas/ \
  -v 2>&1 | grep -i "access-control"
```

**Deberías ver:**
```
< Access-Control-Allow-Origin: http://localhost:3001
< Access-Control-Allow-Methods: DELETE, GET, OPTIONS, POST, PUT
```

### Verificar que el Backend responde

```bash
# Probar endpoint de mesas
curl http://localhost:99/api/mesas/ | python3 -m json.tool

# Probar endpoint de sectores
curl http://localhost:8099/api/sectores/ | python3 -m json.tool
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask_cors'"

**Solución:**
```bash
# Instalar Flask-CORS localmente
pip3 install Flask-CORS==4.0.0

# Si usas Docker, reconstruir la imagen
docker compose build backend
```

### Error: "Network Error" en el Frontend

**Posibles causas:**

1. **CORS no configurado**
   - Verificar que `Flask-CORS` esté instalado
   - Verificar que CORS esté configurado en `app.py`

2. **Backend no está corriendo**
   ```bash
   # Verificar que el backend esté corriendo
   curl http://localhost:99/api/mesas/
   ```

3. **URL incorrecta en el frontend**
   - Verificar `BACKEND_URL` en los servicios
   - Verificar que el puerto sea correcto (99 local, 8099 Docker)

4. **Puerto bloqueado**
   - Verificar que el puerto 99 (o 8099) esté libre
   - Verificar firewall

### Error: "Connection refused"

**Solución:**
```bash
# Verificar que el backend esté corriendo
ps aux | grep python3

# Verificar el puerto
lsof -i :99

# Iniciar el backend
cd backend
python3 app.py
```

### El Frontend no se actualiza (Hot Reload)

**Solución:**
```bash
# Limpiar cache de Vite
cd web
rm -rf node_modules/.vite
pnpm dev
```

### Problemas con Docker

```bash
# Ver logs del contenedor
docker compose logs backend

# Reconstruir todo
docker compose down
docker compose build --no-cache
docker compose up -d

# Verificar que el contenedor esté corriendo
docker ps | grep isfpp-backend
```

---

## 📝 Resumen de Puertos

| Servicio | Puerto Local | Puerto Docker |
|----------|--------------|---------------|
| Backend (Flask) | 99 | 8099 |
| Frontend (Vite) | 3000/3001/3002 | - |
| PostgreSQL | 5432 | 5432 |

---

## ✅ Checklist de Configuración

- [ ] Flask-CORS instalado localmente (`pip3 install Flask-CORS==4.0.0`)
- [ ] Flask-CORS en `requirements.txt`
- [ ] CORS configurado en `backend/app.py`
- [ ] `BACKEND_URL` correcto en servicios del frontend
- [ ] Backend corriendo en puerto 99 (local) o 8099 (Docker)
- [ ] Frontend corriendo y accesible
- [ ] CORS funcionando (verificar con curl)

---

## 🔗 Referencias

- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)

---

**Última actualización:** Noviembre 2025

