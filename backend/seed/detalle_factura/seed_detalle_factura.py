"""
Seeder para detalle_factura
"""
from random import randint
from decimal import Decimal
from models import DetalleFactura, DetalleComanda


def seed_detalles_factura(session, facturas, productos=None):
    """Crea detalles de factura de prueba usando detalles de comanda existentes.

    El modelo `DetalleFactura` requiere `id_detalle_comanda`. Para cada factura
    se asociarán algunos `DetalleComanda` (si existen en la comanda vinculada).

    Args:
        session: sesión de la base de datos
        facturas: lista de Factura
        productos: lista de Producto (opcional, se usa si no hay detalles de comanda)
    Returns:
        lista de DetalleFactura creados
    """
    print("📦 Creando detalles de factura...")

    detalles = []

    for factura in facturas:
        # Obtener detalles de comanda asociados a la comanda de la factura
        id_comanda = getattr(factura, 'id_comanda', None)
        detalles_comanda = []
        if id_comanda is not None:
            detalles_comanda = session.query(DetalleComanda).filter_by(id_comanda=id_comanda).all()

        if not detalles_comanda:
            # Si no hay detalles de comanda, intentar crear desde productos (fallback)
            if not productos:
                productos = session.query(DetalleComanda).all()
            # no hay detalles para usar -> saltar
            continue

        # Para cada detalle de comanda creamos un detalle de factura
        for dc in detalles_comanda:
            cantidad = getattr(dc, 'cantidad', 1)
            precio_unitario = getattr(dc, 'precio_unitario', Decimal('0.00'))
            subtotal = Decimal(cantidad) * Decimal(precio_unitario)

            detalle = DetalleFactura(
                id_factura=getattr(factura, 'id_factura', None),
                id_detalle_comanda=getattr(dc, 'id_detalle_comanda', None),
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal
            )
            detalles.append(detalle)

    if detalles:
        session.add_all(detalles)
        session.commit()

    print(f"✅ {len(detalles)} detalles de factura creados")
    return detalles
