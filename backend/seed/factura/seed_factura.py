"""
Seeder para facturas
"""
from random import randint, choice
from datetime import datetime
from decimal import Decimal
from models import Factura, DetalleComanda


def seed_facturas(session, clientes, comandas=None):
    """Crea facturas de prueba.

    Args:
        session: sesión de la base de datos
        clientes: lista de objetos Cliente ya creados
        comandas: lista opcional de Comanda
    Returns:
        lista de Factura creadas
    """
    print("📦 Creando facturas...")

    facturas = []

    if comandas:
        # Filtrar comandas que tengan al menos un detalle (más realista)
        comandas_con_detalles = []
        for c in comandas:
            # Intentar usar la relación 'detalles' si está cargada
            if getattr(c, 'detalles', None):
                if len(c.detalles) > 0:
                    comandas_con_detalles.append(c)
                    continue
            # Si no está cargada, consultamos DetalleComanda por id_comanda
            id_c = getattr(c, 'id_comanda', None)
            if id_c is not None:
                count = session.query(DetalleComanda).filter_by(id_comanda=id_c).count()
                if count > 0:
                    comandas_con_detalles.append(c)

        # Crear una factura por cada comanda que tenga detalles (o hasta cierto límite)
        for i, c in enumerate(comandas_con_detalles):
            cliente = choice(clientes)
            id_comanda = getattr(c, 'id_comanda', None)
            codigo = f"F-{randint(1000,9999)}-{i}"
            fecha = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            # total por ahora lo tomamos de la comanda si existe, sino aleatorio
            try:
                total_val = Decimal(str(c.calcular_total())) if getattr(c, 'calcular_total', None) else Decimal(f"{randint(100, 2000)}.{randint(0,99):02d}")
            except Exception:
                total_val = Decimal(f"{randint(100, 2000)}.{randint(0,99):02d}")

            factura = Factura(
                codigo=codigo,
                fecha=fecha,
                total=total_val,
                id_cliente=cliente.id_cliente,
                id_comanda=id_comanda,
            )
            facturas.append(factura)
    else:
        # Comportamiento previo si no se pasan comandas: crear facturas aleatorias
        num_facturas = max(5, len(clientes) // 2)
        for i in range(num_facturas):
            cliente = choice(clientes)
            codigo = f"F-{randint(1000,9999)}-{i}"
            fecha = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            total = Decimal(f"{randint(100, 2000)}.{randint(0,99):02d}")

            factura = Factura(
                codigo=codigo,
                fecha=fecha,
                total=total,
                id_cliente=cliente.id_cliente,
                id_comanda=None,
            )
            facturas.append(factura)

    session.add_all(facturas)
    session.commit()
    print(f"✅ {len(facturas)} facturas creadas")
    return facturas
