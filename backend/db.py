import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def ensure_utf8_string(value):
    """
    Asegura que una cadena esté correctamente codificada en UTF-8.
    Útil para evitar problemas de codificación en Windows.
    """
    if value is None:
        return None
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            # Si falla UTF-8, intentar con latin-1 y luego convertir
            return value.decode('latin-1').encode('utf-8').decode('utf-8')
    # Si ya es string, asegurar que esté en UTF-8
    if isinstance(value, str):
        try:
            # Verificar que puede ser codificado en UTF-8
            value.encode('utf-8')
            return value
        except UnicodeEncodeError:
            # Si hay problemas, forzar codificación
            return value.encode('utf-8', errors='ignore').decode('utf-8')
    return str(value)

# Obtener DATABASE_URL de variable de entorno o usar valor por defecto
# En Docker: usa 'database' como hostname
# En local: usa 'localhost' como hostname
if not os.getenv('DATABASE_URL'):
    # Si no hay DATABASE_URL, construirla desde DATABASE_HOST o usar localhost
    db_host = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_URL = f'postgresql://postgres:postgres@{db_host}:5432/postgresIng'
else:
    DATABASE_URL = os.getenv('DATABASE_URL')

# Asegurar que DATABASE_URL esté en UTF-8 (importante para Windows)
DATABASE_URL = ensure_utf8_string(DATABASE_URL)

# Crear engine con configuración optimizada
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_recycle=3600,   # Recicla conexiones cada hora
    echo=False,          # Cambiar a True para ver SQL en consola
    connect_args={
        'client_encoding': 'utf8'  # Forzar codificación UTF-8 en la conexión (importante para Windows)
    }
)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
