import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener URL de BD
db_host = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_URL = os.getenv('DATABASE_URL', f'postgresql://postgres:postgres@{db_host}:5432/postgresIng')

# Usar AUTOCOMMIT para poder ejecutar DROP DATABASE/SCHEMA sin bloqueos de transacción
engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")

def reset_db():
    try:
        with engine.connect() as connection:
            print("🗑️  Eliminando esquema public (DROP SCHEMA public CASCADE)...")
            connection.execute(text("DROP SCHEMA public CASCADE;"))
            
            print("✨ Recreando esquema public...")
            connection.execute(text("CREATE SCHEMA public;"))
            
            print("✅ Base de datos reseteada exitosamente. Ahora está vacía y lista para migraciones.")
    except Exception as e:
        print(f"❌ Error al resetear DB: {e}")

if __name__ == "__main__":
    reset_db()

