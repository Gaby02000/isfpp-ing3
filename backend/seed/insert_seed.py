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
    Sector, Mesa, MedioPago, Cliente, Mozo, Comanda, DetalleComanda, Reserva
)
from models import Factura, DetalleFactura

# Importar seeders
from seed.sector.seed_sector import seed_sectores
from seed.seccion.seed_seccion import seed_secciones
from seed.producto.seed_producto import seed_productos
from seed.mesa.seed_mesa import seed_mesas
from seed.mediopago.seed_medio_pago import seed_medio_pago
from seed.cliente.seed_cliente import seed_clientes
from seed.mozo.seed_mozo import seed_mozos
from seed.comanda.seed_comanda import seed_comandas
from seed.factura.seed_factura import seed_facturas
from seed.detalle_factura.seed_detalle_factura import seed_detalles_factura
from seed.reserva.seed_reserva import seed_reservas


def limpiar_datos(session):
    """Limpia todos los datos existentes"""
    print("⚠️  Limpiando datos existentes...")
    try:
        # Limpiar en orden de dependencias (primero las tablas dependientes)
        # Detalles y facturas
        session.query(DetalleFactura).delete()
        session.query(Factura).delete()
        session.query(Reserva).delete()
        session.query(DetalleComanda).delete()
        session.query(Comanda).delete()
        session.query(Mesa).delete()
        session.query(Mozo).delete()
        session.query(Cliente).delete()
        session.query(Sector).delete()
        session.query(Plato).delete()
        session.query(Postre).delete()
        session.query(Bebida).delete()
        session.query(Producto).delete()
        session.query(Seccion).delete()
        session.query(MedioPago).delete()
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
        mozos = seed_mozos(session, sectores)
        medios_pago = seed_medio_pago(session)
        clientes = seed_clientes(session)
        reservas = seed_reservas(session, clientes, mesas)
        comandas = seed_comandas(session, mozos, mesas, productos)

        # Crear facturas y sus detalles (si hay productos y clientes)
        facturas = seed_facturas(session, clientes, comandas)
        detalles = seed_detalles_factura(session, facturas, productos)

        print("=" * 50)
        print("✅ ¡Carga de datos completada exitosamente!")
        print(f"📊 Resumen:")
        print(f"   - Sectores: {len(sectores)}")
        print(f"   - Secciones: {len(secciones)}")
        print(f"   - Productos: {len(productos)}")
        print(f"   - Mesas: {len(mesas)}")
        print(f"   - Mozos: {len(mozos)}")
        print(f"   - Medios de Pago: {len(medios_pago)}")
        print(f"   - Clientes: {len(clientes)}")
        print(f"   - Reservas: {len(reservas)}")
        print(f"   - Comandas: {len(comandas)}")
        print(f"   - Facturas: {len(facturas)}")
        print(f"   - Detalles de factura: {len(detalles)}")

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

