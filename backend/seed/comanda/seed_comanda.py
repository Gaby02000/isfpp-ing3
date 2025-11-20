"""
Seeder para Comandas
Genera Comandas de prueba asociadas a mozos y mesas existentes
"""
from random import randint, choice
from models import Comanda, Mozo, Mesa

def seed_comandas(session, mozos, mesas, cantidad=20):
    """Crea comandas de prueba"""
    print("📦 Creando comandas...")
    
    comandas = []
    
    for _ in range(cantidad):
        mozo = choice(mozos)
        mesa = choice(mesas)
        
        comanda = Comanda(
            fecha="2024-01-01 12:00:00",
            id_mozo=mozo.id_mozo,
            id_mesa=mesa.id_mesa,
            baja=False
        )
        comandas.append(comanda)
    
    session.add_all(comandas)
    session.commit()
    print(f"✅ {len(comandas)} comandas creadas")
    return comandas