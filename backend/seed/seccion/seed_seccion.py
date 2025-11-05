"""
Seeder para Secciones de Carta
Genera secciones de la carta del restaurante
"""
from models import Seccion


def seed_secciones(session):
    """Crea secciones de la carta"""
    print("📦 Creando secciones de carta...")
    
    secciones = [
        Seccion(nombre="Entradas", baja=False),
        Seccion(nombre="Platos Principales", baja=False),
        Seccion(nombre="Postres", baja=False),
        Seccion(nombre="Bebidas", baja=False),
        Seccion(nombre="Menú del Día", baja=False),
    ]
    
    session.add_all(secciones)
    session.commit()
    print(f"✅ {len(secciones)} secciones creadas")
    return secciones

