FROM node:18-alpine

# Instalar pnpm
RUN npm install -g pnpm

WORKDIR /app

# Copiar archivos del workspace de pnpm (raíz del proyecto)
COPY pnpm-workspace.yaml pnpm-lock.yaml package.json ./

# Copiar package.json de web para que pnpm resuelva las dependencias del workspace
COPY web/package.json ./web/

# Instalar dependencias respetando el workspace
RUN pnpm install --frozen-lockfile

# Copiar el resto de los archivos de web
COPY web/ ./web/

# Cambiar al directorio de web para ejecutar el comando
WORKDIR /app/web

EXPOSE 3000
CMD ["pnpm", "run", "dev"]
