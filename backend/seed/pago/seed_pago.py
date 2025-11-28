from models import Pago, Factura, MedioPago
import random
from faker import Faker

fake = Faker('es_ES')

def seed_pagos(session, facturas, medios_pago):
    """
    Crea pagos para algunas facturas.
    Algunas facturas se pagan completo, otras parcial y otras nada.
    """
    print("💳 Creando pagos...")
    pagos = []
    
    if not facturas or not medios_pago:
        print("⚠️  No hay facturas o medios de pago para crear pagos.")
        return []

    for factura in facturas:
        # 70% de probabilidad de tener algún pago
        if random.random() < 0.7:
            total_factura = float(factura.total)
            
            # 80% de probabilidad de pago total, 20% parcial
            if random.random() < 0.8:
                monto_a_pagar = total_factura
            else:
                # Pago parcial (entre 10% y 90%)
                monto_a_pagar = round(total_factura * random.uniform(0.1, 0.9), 2)
            
            # Seleccionar medio de pago aleatorio
            medio = random.choice(medios_pago)
            
            # Fecha de pago (misma fecha que la factura o un poco después)
            # Simplificamos usando la fecha de la factura
            fecha_pago = factura.fecha
            
            pago = Pago(
                id_factura=factura.id_factura,
                id_medio_pago=medio.id_medio_pago,
                monto=monto_a_pagar,
                fecha=fecha_pago
            )
            session.add(pago)
            pagos.append(pago)
            
    session.commit()
    print(f"✅ {len(pagos)} pagos creados.")
    return pagos

