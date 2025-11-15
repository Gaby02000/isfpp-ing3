"""
Seeder para medios de pago
"""
from random import choice, randint
from models import MedioPago

def seed_medio_pago(session):
    """Crea medios de pago de prueba"""
    print("📦 Creando medios de pago...")
    
    medios_pago = []
    
    nombres_medio_pago = [
        "Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito",
        "Transferencia Bancaria", "Mercado Pago", "PayPal",
        "Criptomonedas", "Cheque", "Vale de Descuento"
    ]
    
    for nombre in nombres_medio_pago:
        descripcion = f"Método de pago mediante {nombre.lower()}."
        medio_pago = MedioPago(
            nombre=nombre,
            descripcion=descripcion,
            baja=False
        )
        medios_pago.append(medio_pago)
    
    session.add_all(medios_pago)
    session.commit()
    print(f"✅ {len(medios_pago)} medios de pago creados")
    return medios_pago