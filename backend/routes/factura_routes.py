from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Factura, DetalleFactura, Comanda, DetalleComanda, Cliente
from datetime import datetime

factura_bp = Blueprint('factura', __name__)

@factura_bp.route('/', methods=['GET'])
def listar_facturas():
    """Lista todas las facturas con paginación"""
    session = SessionLocal()
    try:
        from sqlalchemy import func
        from models import Pago
        
        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        # Filtros
        id_comanda = request.args.get('id_comanda', type=int)
        solo_impagas = request.args.get('solo_impagas', type=str)
        solo_impagas = solo_impagas and solo_impagas.lower() in ('true', '1', 'yes')
        
        # Validar parámetros
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        query = session.query(Factura).filter_by(baja=False).order_by(Factura.fecha.desc())
        
        # Filtrar por id_comanda si se proporciona
        if id_comanda:
            query = query.filter_by(id_comanda=id_comanda)
        
        # Filtrar solo facturas impagas
        if solo_impagas:
            # Subquery para calcular el total pagado por factura
            total_pagado_subq = session.query(
                Pago.id_factura,
                func.sum(Pago.monto).label('total_pagado')
            ).group_by(Pago.id_factura).subquery()
            
            # Query principal con LEFT JOIN para incluir facturas sin pagos
            query = query.outerjoin(
                total_pagado_subq,
                Factura.id_factura == total_pagado_subq.c.id_factura
            ).filter(
                (func.coalesce(total_pagado_subq.c.total_pagado, 0) < Factura.total)
            )
        
        # Contar total
        total = query.count()
        
        # Aplicar paginación
        offset = (page - 1) * per_page
        facturas = query.offset(offset).limit(per_page).all()
        data = [f.json() for f in facturas]
        
        # Calcular total de páginas
        total_pages = (total + per_page - 1) // per_page if total > 0 else 1
        
        return jsonify({
            'status': 'success',
            'data': data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }), 200
    except Exception as e:
        return jsonify({'status':'error', 'message': f'Error al listar facturas: {str(e)}'}), 500
    finally:
        session.close()

@factura_bp.route('/<int:id_factura>', methods=['GET'])
def obtener_factura(id_factura):
    """Obtiene una factura específica"""
    session = SessionLocal()
    try:
        factura = session.query(Factura).filter_by(id_factura=id_factura).first()
        if not factura:
            return jsonify({'status':'error', 'message': f'No existe una factura con id_factura {id_factura}'}), 404
        
        return jsonify({
            'status':'success',
            'data': factura.json()
        }), 200
    except Exception as e:
        return jsonify({'status':'error', 'message': f'Error al obtener la factura: {str(e)}'}), 500
    finally:
        session.close()

@factura_bp.route('/generar-desde-comanda/<int:id_comanda>', methods=['POST'])
def generar_factura_desde_comanda(id_comanda):
    """Genera una factura a partir de una comanda abierta"""
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        
        # Obtener id_cliente del body
        id_cliente = data.get('id_cliente')
        
        # Validar que se proporcionó un cliente
        if not id_cliente:
            return jsonify({
                'status':'error',
                'message': 'Debe seleccionar un cliente para generar la factura'
            }), 400
        
        # Convertir a entero
        try:
            id_cliente = int(id_cliente)
        except (ValueError, TypeError):
            return jsonify({'status':'error', 'message': 'El id_cliente debe ser un número válido'}), 400
        
        # Validar que el cliente existe y está activo
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente, baja=False).first()
        if not cliente:
            return jsonify({
                'status':'error',
                'message': f'No existe un cliente activo con id_cliente {id_cliente}'
            }), 400
        
        # Validar que la comanda existe y está abierta
        comanda = session.query(Comanda).filter_by(id_comanda=id_comanda).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id_comanda}'}), 404
        
        if comanda.estado != 'Abierta':
            return jsonify({
                'status':'error',
                'message': f'No se puede facturar una comanda con estado "{comanda.estado}". Solo se pueden facturar comandas abiertas.'
            }), 400
        
        if comanda.baja:
            return jsonify({'status':'error', 'message': 'No se puede facturar una comanda dada de baja'}), 400
        
        # Validar que la comanda tenga productos
        if not comanda.detalles or len(comanda.detalles) == 0:
            return jsonify({'status':'error', 'message': 'La comanda no tiene productos para facturar'}), 400
        
        # Calcular total
        total = comanda.calcular_total()
        
        # Generar código único de factura (formato: FACT-YYYYMMDD-XXXXX)
        fecha_actual = datetime.now()
        fecha_str = fecha_actual.strftime('%Y%m%d')
        # Buscar el último número de factura del día
        ultima_factura = session.query(Factura).filter(
            Factura.codigo.like(f'FACT-{fecha_str}-%')
        ).order_by(Factura.codigo.desc()).first()
        
        if ultima_factura:
            ultimo_numero = int(ultima_factura.codigo.split('-')[-1])
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1
        
        codigo_factura = f'FACT-{fecha_str}-{nuevo_numero:05d}'
        
        # Crear factura
        nueva_factura = Factura(
            codigo=codigo_factura,
            fecha=fecha_actual.strftime('%Y-%m-%d %H:%M:%S'),
            total=total,
            id_comanda=id_comanda,
            id_cliente=id_cliente
        )
        session.add(nueva_factura)
        session.flush()  # Para obtener el id_factura
        
        # Crear detalles de factura a partir de los detalles de comanda
        for detalle_comanda in comanda.detalles:
            detalle_factura = DetalleFactura(
                id_factura=nueva_factura.id_factura,
                id_detalle_comanda=detalle_comanda.id_detalle_comanda,
                cantidad=detalle_comanda.cantidad,
                precio_unitario=detalle_comanda.precio_unitario,
                subtotal=detalle_comanda.precio_unitario * detalle_comanda.cantidad
            )
            session.add(detalle_factura)
        
        # Cambiar estado de la comanda a "Cerrada"
        comanda.estado = 'Cerrada'
        comanda.fecha_cierre = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')
        
        session.commit()
        
        return jsonify({
            'status':'success',
            'message': 'Factura generada exitosamente',
            'data': nueva_factura.json()
        }), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al generar la factura: {str(e)}'}), 500
    finally:
        session.close()

@factura_bp.route('/<int:id>', methods=['DELETE'])
def anular_factura(id):
    """Anula una factura (baja lógica)"""
    session = SessionLocal()
    try:
        factura = session.query(Factura).filter_by(id_factura=id).first()
        if not factura:
            return jsonify({'status':'error', 'message': f'No existe una factura con id_factura {id}'}), 404
        
        if factura.baja:
            return jsonify({'status':'error', 'message': 'La factura ya está anulada'}), 400
        
        # Anular factura
        factura.baja = True
        
        # Opcionalmente: reabrir la comanda
        # comanda = factura.comanda
        # if comanda:
        #     comanda.estado = 'Abierta'
        #     comanda.fecha_cierre = None
        
        session.commit()
        
        return jsonify({
            'status':'success',
            'message': 'Factura anulada exitosamente',
            'data': factura.json()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al anular la factura: {str(e)}'}), 500
    finally:
        session.close()