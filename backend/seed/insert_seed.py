"""
Script principal para cargar datos falsos en la base de datos.
Ejecutar con: python3 -m seed.insert_seed
O con pnpm: pnpm seed
"""
import sys
import os

# Agregar el directorio padre al path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from db import SessionLocal, engine, Base
from models import (
    Seccion, Producto, Plato, Postre, Bebida,
    Sector, Mesa
)

# Importar seeders
from seed.sector.seed_sector import seed_sectores
from seed.seccion.seed_seccion import seed_secciones
from seed.producto.seed_producto import seed_productos
from seed.mesa.seed_mesa import seed_mesas


def limpiar_datos(session):
    """Limpia todos los datos existentes"""
    print("⚠️  Limpiando datos existentes...")
    try:
        session.query(Mesa).delete()
        session.query(Sector).delete()
        session.query(Plato).delete()
        session.query(Postre).delete()
        session.query(Bebida).delete()
        session.query(Producto).delete()
        session.query(Seccion).delete()
        session.commit()
        print("✅ Datos limpiados")
    except Exception as e:
        session.rollback()
        print(f"⚠️  Error al limpiar datos: {str(e)}")
        print("   Continuando con la carga...")


def main():
    """Función principal que ejecuta todos los seeders"""
    print("🌱 Iniciando carga de datos falsos...")
    print("=" * 50)
    
    # Crear todas las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    
    try:
        # Limpiar datos existentes (opcional - comentar si no quieres borrar)
        limpiar_datos(session)
        
        # Crear datos en orden de dependencias
        sectores = seed_sectores(session)
        secciones = seed_secciones(session)
        productos = seed_productos(session, secciones)
        mesas = seed_mesas(session, sectores)
        
        print("=" * 50)
        print("✅ ¡Carga de datos completada exitosamente!")
        print(f"📊 Resumen:")
        print(f"   - Sectores: {len(sectores)}")
        print(f"   - Secciones: {len(secciones)}")
        print(f"   - Productos: {len(productos)}")
        print(f"   - Mesas: {len(mesas)}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error al cargar datos: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()

