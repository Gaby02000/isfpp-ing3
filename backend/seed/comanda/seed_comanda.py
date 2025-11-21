"""
Seeder para Comandas
Genera Comandas de prueba asociadas a mozos y mesas existentes
"""
from random import randint, choice
from models import Comanda, Mozo, Mesa, Producto, DetalleComanda
from datetime import datetime, timedelta

def seed_comandas(session, mozos, mesas, productos=None, cantidad=20):
    """Crea comandas de prueba"""
    print("📦 Creando comandas...")
    
    if productos is None:
        productos = session.query(Producto).filter_by(baja=False).all()
    
    comandas = []
    base_date = datetime(2024, 1, 1, 12, 0, 0)
    
    for i in range(cantidad):
        mozo = choice(mozos)
        mesa = choice(mesas)
        
        # Generar fecha variada
        fecha = (base_date + timedelta(days=i, hours=randint(0, 10))).strftime('%Y-%m-%d %H:%M:%S')
        
        # Determinar estado (mayoría abiertas, algunas cerradas)
        if i < cantidad * 0.7:  # 70% abiertas
            estado = 'Abierta'
            fecha_cierre = None
        else:  # 30% cerradas
            estado = 'Cerrada'
            fecha_cierre = (base_date + timedelta(days=i, hours=randint(11, 15))).strftime('%Y-%m-%d %H:%M:%S')
        
        comanda = Comanda(
            fecha=fecha,
            fecha_cierre=fecha_cierre,
            id_mozo=mozo.id,  # CORREGIDO: usar 'id' en lugar de 'id_mozo'
            id_mesa=mesa.id_mesa,
            estado=estado,
            baja=False
        )
        session.add(comanda)
        session.flush()  # Para obtener el id_comanda
        
        # Agregar productos aleatorios a la comanda
        if productos:
            num_productos = randint(1, 5)
            productos_seleccionados = [choice(productos) for _ in range(num_productos)]
            
            for producto in productos_seleccionados:
                cantidad = randint(1, 3)
                entregado = estado == 'Cerrada'  # Si está cerrada, todos entregados
                
                detalle = DetalleComanda(
                    id_comanda=comanda.id_comanda,
                    id_producto=producto.id_producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                    entregado=entregado
                )
                session.add(detalle)
        
        comandas.append(comanda)
    
    session.commit()
    print(f"✅ {len(comandas)} comandas creadas")
    return comandas