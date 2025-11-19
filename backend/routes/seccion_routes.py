from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Seccion

seccion_bp = Blueprint('seccion', __name__)

@seccion_bp.route('/', methods=['GET'])
def listar_secciones():
    session = SessionLocal()
    try:
        activos = request.args.get('activos', '').lower() == 'true'
        
        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        # Validar parámetros de paginación
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        query = session.query(Seccion)
        
        # Filtros
        if activos == 'true':
            query = query.filter_by(baja=False)
        elif activos == 'false':
            query = query.filter_by(baja=True)
        else:
            # Por defecto solo mostrar activos
            query = query.filter_by(baja=False)
        
        # Ordenamiento por nombre
        query = query.order_by(Seccion.nombre)
        
        # Contar total antes de paginar
        total = query.count()
        
        # Aplicar paginación
        offset = (page - 1) * per_page
        secciones = query.offset(offset).limit(per_page).all()
        
        data = [s.json() for s in secciones]
        
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
            'message': f'Error al listar secciones: {str(e)}'
        }), 500
    finally:
        session.close()


@seccion_bp.route('/', methods=['POST'])
def crear_seccion():
    session = SessionLocal()
    data = request.get_json()
    if not data or 'nombre' not in data:
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'El campo "nombre" es requerido'
        }), 200

    nueva = Seccion(nombre=data['nombre'], baja=False)
    session.add(nueva)
    session.commit()
    res = nueva.json()
    session.close()
    return jsonify({
        'status': 'success',
        'message': 'Sección creada correctamente',
        'data': res
    }), 200


@seccion_bp.route('/<int:id>', methods=['GET'])
def obtener_seccion(id):
    session = SessionLocal()
    seccion = session.query(Seccion).get(id)
    session.close()
    if not seccion or seccion.baja:
        return jsonify({
            'status': 'error',
            'message': 'Sección no encontrada'
        }), 200
    return jsonify({
        'status': 'success',
        'data': seccion.json()
    }), 200


@seccion_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_seccion(id):
    session = SessionLocal()
    seccion = session.query(Seccion).get(id)
    if not seccion or seccion.baja:
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Sección no encontrada o ya dada de baja'
        }), 200
    
    seccion.baja = True
    session.commit()
    res = seccion.json()
    session.close()
    return jsonify({
        'status': 'success',
        'message': 'Sección dada de baja correctamente',
        'data': res
    }), 200