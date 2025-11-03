# isfpp-ing3

## 🚀 Instalación y Setup

Este proyecto utiliza **pnpm** como gestor de dependencias.

### Requisitos previos

- Node.js 18+
- pnpm (instalar globalmente: `npm install -g pnpm`)
- Docker y Docker Compose (para desarrollo con contenedores)
- Python 3.8+ (para desarrollo local del backend)

### Instalación

1. **Instalar pnpm** (si no lo tienes):
```bash
npm install -g pnpm
```

2. **Instalar dependencias**:
```bash
pnpm install           # Instala todas las dependencias (frontend + backend)
pnpm run install:all   # Equivalente a pnpm install
```

## 📋 Comandos disponibles

### Desde la raíz del proyecto:

**🚀 Desarrollo local (sin Docker) - RECOMENDADO:**
```bash
pnpm dev              # Levanta frontend y backend en paralelo
pnpm run dev:frontend # Solo frontend (http://localhost:3000)
pnpm run dev:backend  # Solo backend (http://localhost:99)
```

**🐳 Docker (contenedores):**
```bash
pnpm start            # Levantar todo (frontend + backend + base de datos)
pnpm run start:build  # Levantar con reconstrucción de imágenes
pnpm run stop         # Detener sin eliminar volúmenes
pnpm run stop:volumes # Detener y eliminar volúmenes
pnpm run backend      # Solo backend + base de datos
pnpm run frontend     # Solo frontend
```

**📊 Logs y estado:**
```bash
pnpm run logs          # Ver todos los logs
pnpm run logs:backend  # Ver solo logs del backend
pnpm run logs:frontend # Ver solo logs del frontend
pnpm run status        # Ver estado de los contenedores
pnpm run restart       # Reiniciar servicios
```

**🔨 Build y lint:**
```bash
pnpm build            # Build del frontend
pnpm lint             # Linter del frontend
```

### Desde la carpeta `web/`:

**Desarrollo del frontend:**
```bash
pnpm dev            # Desarrollo normal (usa VITE_BACKEND_URL de env)
pnpm run dev:local  # Desarrollo apuntando a localhost:8099
```

**Build y preview:**
```bash
pnpm build      # Build de producción
pnpm preview    # Preview del build
pnpm lint       # Linter
```

### Desde la carpeta `backend/`:

**Desarrollo del backend:**
```bash
pnpm dev              # Inicia Flask en modo desarrollo
pnpm run install:python  # Instala dependencias Python (pip3 install -r requirements.txt)
```

## 🌐 URLs de acceso:

- Frontend: http://localhost:3000
- Backend: http://localhost:8099
- Base de datos: localhost:5432

## 📝 Notas

- Para desarrollo local sin Docker, asegúrate de tener:
  - Python 3.8+ instalado (verificar con `python3 --version`)
  - Dependencias del backend instaladas (`pip3 install -r backend/requirements.txt` o `cd backend && pnpm run install:python`)
  - Base de datos PostgreSQL corriendo en localhost:5432
- El proyecto usa **pnpm** para mejor rendimiento y gestión de dependencias
- El archivo `pnpm-lock.yaml` se versiona para mantener consistencia entre entornos