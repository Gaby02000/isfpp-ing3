"""
Seeder para Mesas
Genera mesas de prueba distribuidas en los sectores
"""
from random import choice, randint
from models import Mesa


def seed_mesas(session, sectores):
    """Crea mesas de prueba"""
    print("📦 Creando mesas...")
    
    mesas = []
    numero_mesa = 1
    
    tipos_mesa = ["Individual", "Pareja", "Cuadrada", "Redonda", "Rectangular"]
    
    for sector in sectores:
        # Crear 4-6 mesas por sector
        cant_mesas_sector = randint(4, 6)
        for i in range(cant_mesas_sector):
            tipo = choice(tipos_mesa)
            cant_comensales = randint(2, 8)
            
            mesa = Mesa(
                numero=numero_mesa,
                tipo=tipo,
                cant_comensales=cant_comensales,
                id_sector=sector.id_sector,
                baja=False
            )
            mesas.append(mesa)
            numero_mesa += 1
    
    session.add_all(mesas)
    session.commit()
    print(f"✅ {len(mesas)} mesas creadas")
    return mesas

