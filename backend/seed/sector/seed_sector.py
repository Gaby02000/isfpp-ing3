"""
Seeder para Sectores
Genera sectores de prueba para el restaurante
"""
from models import Sector


def seed_sectores(session):
    """Crea sectores de prueba"""
    print("📦 Creando sectores...")
    
    sectores = [
        Sector(numero=1, baja=False),
        Sector(numero=2, baja=False),
        Sector(numero=3, baja=False),
        Sector(numero=4, baja=False),
        Sector(numero=5, baja=False),
    ]
    
    session.add_all(sectores)
    session.commit()
    print(f"✅ {len(sectores)} sectores creados")
    return sectores

