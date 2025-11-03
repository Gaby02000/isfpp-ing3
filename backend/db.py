import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener DATABASE_URL de variable de entorno o usar valor por defecto
# En Docker: usa 'database' como hostname
# En local: usa 'localhost' como hostname
if not os.getenv('DATABASE_URL'):
    # Si no hay DATABASE_URL, construirla desde DATABASE_HOST o usar localhost
    db_host = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_URL = f'postgresql://postgres:postgres@{db_host}:5432/postgresIng'
else:
    DATABASE_URL = os.getenv('DATABASE_URL')

# Crear engine con configuración optimizada
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_recycle=3600,   # Recicla conexiones cada hora
    echo=False           # Cambiar a True para ver SQL en consola
)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
