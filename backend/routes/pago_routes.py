from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Pago, Factura, MedioPago

pago_bp = Blueprint('pago', __name__)

@pago_bp.route('/', methods=['GET'])
def listar_pagos():
    session = SessionLocal()
    try:
        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        # Filtros
        id_medio_pago = request.args.get('id_medio_pago', type=int)
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        search = request.args.get('search')

        # Validar parámetros
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
            
        query = session.query(Pago).join(Factura).order_by(Pago.fecha.desc())
        
        if id_medio_pago:
            query = query.filter(Pago.id_medio_pago == id_medio_pago)
            
        if fecha_desde:
            query = query.filter(Pago.fecha >= fecha_desde)
            
        if fecha_hasta:
            # Asumiendo que fecha es string YYYY-MM-DD HH:MM:SS, si fecha_hasta es YYYY-MM-DD, agregamos hora final
            if len(fecha_hasta) == 10:
                fecha_hasta += ' 23:59:59'
            query = query.filter(Pago.fecha <= fecha_hasta)
            
        if search:
            search = f"%{search}%"
            # Buscar por código de factura o ID de pago
            query = query.filter(
                (Factura.codigo.ilike(search)) | 
                (Pago.id_pago.cast(str).ilike(search))
            )
        
        # Contar total
        total = query.count()
        
        # Aplicar paginación
        offset = (page - 1) * per_page
        pagos = query.offset(offset).limit(per_page).all()
        data = [p.json() for p in pagos]
        
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
        return jsonify({'status':'error','message':f'Error al listar pagos: {str(e)}'}), 500
    finally:
        session.close()

@pago_bp.route('/', methods=['POST'])
def crear_pago():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status':'error','message':'No se proporcionaron datos'}), 400

        id_factura = data.get('id_factura')
        id_medio_pago = data.get('id_medio_pago')
        monto = data.get('monto')
        fecha = data.get('fecha')

        # Validaciones básicas
        if not id_factura or not id_medio_pago or monto is None or not fecha:
            return jsonify({'status':'error','message':'Faltan campos requeridos'}), 400

        try:
            id_factura = int(id_factura)
            id_medio_pago = int(id_medio_pago)
            monto = float(monto)
        except (ValueError, TypeError):
            return jsonify({'status':'error','message':'Campos en formato inválido'}), 400

        # Validar existencia de factura y medio de pago
        factura = session.query(Factura).filter_by(id_factura=id_factura).first()
        if not factura:
            return jsonify({'status':'error','message':f'No existe factura con id {id_factura}'}), 400
        medio = session.query(MedioPago).filter_by(id_medio_pago=id_medio_pago).first()
        if not medio:
            return jsonify({'status':'error','message':f'No existe medio de pago con id {id_medio_pago}'}), 400

        pago = Pago(id_factura=id_factura, id_medio_pago=id_medio_pago, monto=monto, fecha=fecha)
        session.add(pago)
        session.commit()
        return jsonify({'status':'success','message':'Pago creado','data':pago.json()}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error','message':f'Error al crear pago: {str(e)}'}), 500
    finally:
        session.close()

@pago_bp.route('/<int:id_pago>', methods=['GET'])
def obtener_pago(id_pago):
    session = SessionLocal()
    try:
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()
        if not pago:
            return jsonify({'status':'error','message':f'No existe pago con id {id_pago}'}), 404
        return jsonify({'status':'success','data':pago.json()}), 200
    except Exception as e:
        return jsonify({'status':'error','message':f'Error al obtener pago: {str(e)}'}), 500
    finally:
        session.close()

@pago_bp.route('/<int:id_pago>', methods=['PUT'])
def modificar_pago(id_pago):
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status':'error','message':'No se proporcionaron datos'}), 400
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()
        if not pago:
            return jsonify({'status':'error','message':f'No existe pago con id {id_pago}'}), 404

        monto = data.get('monto')
        fecha = data.get('fecha')
        if monto is not None:
            try:
                pago.monto = float(monto)
            except (ValueError, TypeError):
                return jsonify({'status':'error','message':'monto inválido'}), 400
        if fecha is not None:
            pago.fecha = fecha

        session.commit()
        return jsonify({'status':'success','message':'Pago actualizado','data':pago.json()}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error','message':f'Error al modificar pago: {str(e)}'}), 500
    finally:
        session.close()

@pago_bp.route('/<int:id_pago>', methods=['DELETE'])
def eliminar_pago(id_pago):
    session = SessionLocal()
    try:
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()
        if not pago:
            return jsonify({'status':'error','message':f'No existe pago con id {id_pago}'}), 404
        session.delete(pago)
        session.commit()
        return jsonify({'status':'success','message':'Pago eliminado'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error','message':f'Error al eliminar pago: {str(e)}'}), 500
    finally:
        session.close()
