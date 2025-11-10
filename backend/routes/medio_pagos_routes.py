from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import MedioPago

medio_pagos_bp = Blueprint('medio_pagos', __name__)

@medio_pagos_bp.route('/', methods=['GET'])
def listar_medio_pago():
    session = SessionLocal()
    try:

        nombre = request.args.get('nombre', type=str)
        descripcion = request.args.get('descripcion', type=str)
        estado = request.args.get('estado', type=str)  # 'activa' o 'baja'
        ordenar_por = request.args.get('ordenar_por', default='nombre', type=str)

        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        # Validar parámetros de paginación
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        query = session.query(MedioPago)

         # Filtros
        if nombre:
            query = query.filter_by(nombre=nombre)
        if descripcion:
            query = query.filter_by(descripcion=descripcion)
        if estado == 'activa':
            query = query.filter_by(baja=False)
        elif estado == 'baja':
            query = query.filter_by(baja=True)
        else:
            # Por defecto solo mostrar activas
            query = query.filter_by(baja=False)

        # Ordenamiento
        if ordenar_por == 'nombre':
            query = query.order_by(MedioPago.nombre)
        
        # Contar total antes de paginar
        total = query.count()

        # Aplicar paginación
        offset = (page - 1) * per_page
        medio_pago = query.offset(offset).limit(per_page).all()
        data = [m.json() for m in medio_pago]
        
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
        return jsonify({
            'status': 'error',
            'message': f'Error al listar medios de pago: {str(e)}'
        }), 500
    finally:
        session.close()

@medio_pagos_bp.route('/', methods=['POST'])
def crear_medio_pago(): 
    session = SessionLocal()
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
        
        #validar campos obligatorios
        campos_requeridos = ['nombre']
        for campo in campos_requeridos:
            if campo not in data or data:
                return jsonify({
                    'status': 'error',
                    'message': f'El campo "{campo}" es requerido'
                }), 400
        
        #validar tipos de datos
        if not isinstance(data['nombre'], str) or ( 'descripcion' in data and not isinstance(data['descripcion'], str)):
            return jsonify({
                'status': 'error',
                'message': 'Tipo de dato inválido para uno o más campos'
            }), 400
        
        #validar duplicados: nombre o id_medio_pago
        if 'id_medio_pago' in data:
            medio_pago_existente = session.query(MedioPago).filter_by(id_medio_pago=data['id_medio_pago']).first()
            if medio_pago_existente:
                return jsonify({
                    'status': 'error',
                    'message': f'Ya existe un medio de pago con id_medio_pago {data["id_medio_pago"]}'
                }), 400
        
        medio_pago_existente = session.query(MedioPago).filter_by(nombre=data['nombre']).first()
        if medio_pago_existente:
            return jsonify({
                'status': 'error',
                'message': f'Ya existe un medio de pago con nombre {data["nombre"]}'
            }), 400
        
        #crear medio de pago
        nuevo_medio_pago = MedioPago(nombre=data['nombre'], descripcion=data.get('descripcion'), baja=False)

        session.add(nuevo_medio_pago)
        session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Medio de pago creado exitosamente',
            'data': nuevo_medio_pago.json()
        }), 201

    except Exception as e:
            session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'Error al crear medio de pago: {str(e)}'
        }), 500
    finally:
        session.close()

@medio_pagos_bp.route('/<int:id_medio_pago>', methods=['GET'])
def obtener_medio_pago(id_medio_pago):
    session = SessionLocal()
    try:
        medio_pago = session.query(MedioPago).get(id_medio_pago)

        if not medio_pago:
            return jsonify({
                'status': 'error',
                'message': 'No se encontró el medio de pago'
            }), 404
        return jsonify({
            'status': 'success', 
            'data': medio_pago.json()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener medio de pago: {str(e)}'
        }), 500
    finally:
        session.close()

@medio_pagos_bp.route('/<int:id_medio_pago>', methods=['PUT'])
def modificar_medio_pago(id_medio_pago):
    session = SessionLocal()
    try:
        data = request.get_json()
        medio_pago = session.query(MedioPago).get(id_medio_pago)

        if not medio_pago:
            return jsonify({
                'status': 'error',
                'message': 'Medio de pago no encontrado'
            }), 400

        if medio_pago.baja:
            return jsonify({
                'status': 'error',
                'message': 'No se puede modificar un medio de pago dado de baja'
            }), 404
        
        # Validar cambios en campos
        if 'nombre' in data:
            medio_pago_duplicado = session.query(MedioPago).filter_by(nombre=data['nombre']).first()
            if medio_pago_duplicado and medio_pago_duplicado.id_medio_pago != id_medio_pago:
                return jsonify({
                    'status': 'error',
                    'message': f'Ya existe un medio de pago con ese nombre"]'
                }), 400
        
        session.commit()

        return jsonify({
            'status': 'success',    
            'message': 'Medio de pago modificado exitosamente',
            'data': medio_pago.json()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al modificar medio de pago: {str(e)}'
        }), 500
    finally:
        session.close()

@medio_pagos_bp.route('/<int:id_medio_pago>', methods=['DELETE'])
def eliminar_medio_pago(id_medio_pago):
    session = SessionLocal()
    try:
        medio_pago = session.query(MedioPago).get(id_medio_pago)

        if not medio_pago:
            return jsonify({
                'status': 'error',
                'message': 'Medio de pago no encontrado'
            }), 404

        if medio_pago.baja:
            return jsonify({
                'status': 'error',
                'message': 'El medio de pago ya está dado de baja'
            }), 400
        
        medio_pago.baja = True
        session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Medio de pago dado de baja exitosamente',
            'data': medio_pago.json()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al dar de baja el medio de pago: {str(e)}'
        }), 500
    finally:
        session.close()