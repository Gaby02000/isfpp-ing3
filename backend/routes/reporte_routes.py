from flask import Blueprint, jsonify
from sqlalchemy import func, cast,TIMESTAMP
from db import SessionLocal

from models import (
    Factura, 
    DetalleFactura,
    Producto,
    MedioPago,
    Pago,
    Comanda,
    DetalleComanda,
    Reserva,
    Mesa,
    Sector,
    Mozo
)

reporte_bp = Blueprint("reportes", __name__)

# ======================================================
#  1) VENTAS MENSUALES
# ======================================================
@reporte_bp.route("/ventas/mensuales", methods=["GET"])
def ventas_mensuales():
    session = SessionLocal()
    try:
        resultados = (
            session.query(
                func.date_trunc(
                    'month',
                    cast(Factura.fecha, TIMESTAMP)  # <-- aquí hacemos el cast
                ).label("mes"),
                func.sum(Factura.total).label("total")
            )
            .group_by(func.date_trunc('month', cast(Factura.fecha, TIMESTAMP)))
            .order_by(func.date_trunc('month', cast(Factura.fecha, TIMESTAMP)))
            .all()
        )

        data = [
            {"mes": str(r.mes.date()), "total": float(r.total)}
            for r in resultados
        ]

        return jsonify({"status": "success", "data": data}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en ventas mensuales: {str(e)}"}), 500
    finally:
        session.close()

# ======================================================
#  2) PRODUCTOS MÁS VENDIDOS
# ======================================================

@reporte_bp.route("/productos/mas-vendidos", methods=["GET"])
def productos_mas_vendidos():
    session = SessionLocal()
    try:
        # Hacemos join desde DetalleFactura -> DetalleComanda -> Producto
        resultados = (
            session.query(
                Producto.nombre,
                func.sum(DetalleFactura.cantidad).label("cantidad_vendida")
            )
            .join(DetalleComanda, DetalleFactura.id_detalle_comanda == DetalleComanda.id_detalle_comanda)
            .join(Producto, DetalleComanda.id_producto == Producto.id_producto)
            .group_by(Producto.nombre)
            .order_by(func.sum(DetalleFactura.cantidad).desc())
            .limit(10)
            .all()
        )

        data = [
            {"producto": r.nombre, "cantidad": int(r.cantidad_vendida)}
            for r in resultados
        ]

        return jsonify({"status": "success", "data": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en productos más vendidos: {str(e)}"}), 500
    finally:
        session.close()

# ======================================================
#  3) RESERVAS POR DÍA
# ======================================================
@reporte_bp.route("/reservas/por-dia", methods=["GET"])
def reservas_por_dia():
    session = SessionLocal()
    try:
        resultados = (
            session.query(
                Reserva.fecha_hora,
                func.count(Reserva.id_reserva).label("cantidad")
            )
            .group_by(Reserva.fecha_hora)
            .order_by(Reserva.fecha_hora)
            .all()
        )

        data = [
            {"fecha": str(r.fecha_hora), "cantidad": int(r.cantidad)}
            for r in resultados
        ]

        return jsonify({"status": "success", "data": data}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en reservas por día: {str(e)}"}), 500
    finally:
        session.close()


# ======================================================
#  4) MEDIOS DE PAGO
# ======================================================
@reporte_bp.route("/medios-pago", methods=["GET"])
def medios_pago_usados():
    session = SessionLocal()
    try:
        resultados = (
            session.query(
                MedioPago.nombre,
                func.sum(Pago.monto).label("total"),
                func.count(Pago.id_pago).label("cantidad")
            )
            .join(Pago, MedioPago.id_medio_pago == Pago.id_medio_pago)
            .group_by(MedioPago.nombre)
            .all()
        )

        data = [
            {
                "medio_pago": r.nombre,
                "total": float(r.total),
                "cantidad": int(r.cantidad)
            }
            for r in resultados
        ]

        return jsonify({"status": "success", "data": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en medios de pago: {str(e)}"}), 500
    finally:
        session.close()


# ======================================================
#  5) USO DE SECTORES
# ======================================================
@reporte_bp.route("/sectores/uso", methods=["GET"])
def uso_sectores():
    session = SessionLocal()
    try:
        resultados = (
            session.query(
                Sector.numero.label("sector_numero"),
                func.count(Mesa.id_mesa).label("uso")
            )
            .join(Mesa, Sector.id_sector == Mesa.id_sector)
            .join(Comanda, Comanda.id_mesa == Mesa.id_mesa)
            .group_by(Sector.numero)
            .all()
        )

        data = [
            {"sector": r.sector_numero, "uso": int(r.uso)}
            for r in resultados
        ]

        return jsonify({"status": "success", "data": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en uso de sectores: {str(e)}"}), 500
    finally:
        session.close()

# ======================================================
#  6) FACTURACIÓN DE MOZOS
# ======================================================
@reporte_bp.route("/mozos/facturacion", methods=["GET"])
def facturacion_mozos():
    session = SessionLocal()
    try:
        resultados = (
            session.query(
                Mozo.nombre_apellido.label("mozo_nombre"),
                func.sum(Factura.total).label("total_facturado")
            )
            .join(Comanda, Mozo.id == Comanda.id_mozo)
            .join(Factura, Factura.id_comanda == Comanda.id_comanda)
            .group_by(Mozo.nombre_apellido)
            .order_by(func.sum(Factura.total).desc())
            .all()
        )

        data = [
            {"mozo": r.mozo_nombre, "facturado": float(r.total_facturado)}
            for r in resultados
        ]

        return jsonify({"status": "success", "data": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener facturación de mozos: {str(e)}"}), 500
    finally:
        session.close()
