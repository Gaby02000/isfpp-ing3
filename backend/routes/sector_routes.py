from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Sector, Mesa

sector_bp = Blueprint('sector', __name__)

@sector_bp.route('/', methods=['GET'])
def listar_sectores():
    session = SessionLocal()
    try:
        estado = request.args.get('estado', type=str)  # 'activo' o 'baja'
        
        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        # Validar parámetros de paginación
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        query = session.query(Sector)
        
        if estado == 'activo':
            query = query.filter_by(baja=False)
        elif estado == 'baja':
            query = query.filter_by(baja=True)
        else:
            # Por defecto solo mostrar activos
            query = query.filter_by(baja=False)
        
        # Contar total antes de paginar
        total = query.count()
        
        # Aplicar paginación
        offset = (page - 1) * per_page
        sectores = query.offset(offset).limit(per_page).all()
        
        data = []
        for s in sectores:
            sector_data = s.json()
            # Contar mesas activas del sector
            mesas_activas = session.query(Mesa).filter_by(
                id_sector=s.id_sector,
                baja=False
            ).count()
            sector_data['cantidad_mesas'] = mesas_activas
            data.append(sector_data)
        
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
            'message': f'Error al listar sectores: {str(e)}'
        }), 500
    finally:
        session.close()


@sector_bp.route('/todos', methods=['GET'])
def listar_todos_sectores():
    """Endpoint para obtener todos los sectores activos sin paginación (para usar en selects)"""
    session = SessionLocal()
    try:
        query = session.query(Sector).filter_by(baja=False).order_by(Sector.numero)
        sectores = query.all()
        
        data = []
        for s in sectores:
            sector_data = s.json()
            # Contar mesas activas del sector
            mesas_activas = session.query(Mesa).filter_by(
                id_sector=s.id_sector,
                baja=False
            ).count()
            sector_data['cantidad_mesas'] = mesas_activas
            data.append(sector_data)
        
        return jsonify({
            'status': 'success',
            'data': data
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al listar sectores: {str(e)}'
        }), 500
    finally:
        session.close()


@sector_bp.route('/', methods=['POST'])
def crear_sector():
    session = SessionLocal()
    try:
        data = request.get_json()
        
        if not data or 'numero' not in data:
            return jsonify({
                'status': 'error',
                'message': 'El campo "numero" es requerido'
            }), 400
        
        # Validar duplicados
        sector_existente = session.query(Sector).filter_by(numero=data['numero']).first()
        if sector_existente:
            return jsonify({
                'status': 'error',
                'message': 'Ya existe un sector con ese número'
            }), 400
        
        nuevo_sector = Sector(
            numero=data['numero'],
            baja=False
        )
        
        session.add(nuevo_sector)
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Sector creado correctamente',
            'data': nuevo_sector.json()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al crear sector: {str(e)}'
        }), 500
    finally:
        session.close()


@sector_bp.route('/<int:id>', methods=['GET'])
def obtener_sector(id):
    session = SessionLocal()
    try:
        sector = session.query(Sector).get(id)
        
        if not sector:
            return jsonify({
                'status': 'error',
                'message': 'Sector no encontrado'
            }), 404
        
        sector_data = sector.json()
        mesas_activas = session.query(Mesa).filter_by(
            id_sector=sector.id_sector,
            baja=False
        ).count()
        sector_data['cantidad_mesas'] = mesas_activas
        
        return jsonify({
            'status': 'success',
            'data': sector_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener sector: {str(e)}'
        }), 500
    finally:
        session.close()


@sector_bp.route('/<int:id>', methods=['PUT'])
def modificar_sector(id):
    session = SessionLocal()
    try:
        data = request.get_json()
        sector = session.query(Sector).get(id)
        
        if not sector:
            return jsonify({
                'status': 'error',
                'message': 'Sector no encontrado'
            }), 404
        
        if sector.baja:
            return jsonify({
                'status': 'error',
                'message': 'No se puede modificar un sector dado de baja'
            }), 400
        
        if 'numero' in data:
            # Validar que el nuevo número no esté duplicado
            sector_duplicado = session.query(Sector).filter_by(numero=data['numero']).first()
            if sector_duplicado and sector_duplicado.id_sector != id:
                return jsonify({
                    'status': 'error',
                    'message': 'Ya existe otro sector activo con ese número'
                }), 400
            sector.numero = data['numero']
        
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Sector modificado correctamente',
            'data': sector.json()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al modificar sector: {str(e)}'
        }), 500
    finally:
        session.close()


@sector_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_sector(id):
    session = SessionLocal()
    try:
        sector = session.query(Sector).get(id)
        
        if not sector:
            return jsonify({
                'status': 'error',
                'message': 'Sector no encontrado'
            }), 404
        
        if sector.baja:
            return jsonify({
                'status': 'error',
                'message': 'El sector ya está dado de baja'
            }), 400
        
        # Validar que no tenga mesas o mozos activos
        mesas_activas = session.query(Mesa).filter_by(
            id_sector=sector.id_sector,
            baja=False
        ).count()
        
        if mesas_activas > 0:
            return jsonify({
                'status': 'error',
                'message': f'No se puede dar de baja un sector con {mesas_activas} mesa(s) activa(s). Primero debe reasignarse o darse de baja las mesas.'
            }), 400
        
        # TODO: Validar mozos activos cuando exista el modelo Mozo
        # mozos_activos = session.query(Mozo).filter_by(id_sector=sector.id_sector, baja=False).count()
        # if mozos_activos > 0:
        #     return jsonify({
        #         'status': 'error',
        #         'message': f'No se puede dar de baja un sector con {mozos_activos} mozo(s) activo(s).'
        #     }), 400
        
        sector.baja = True
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Sector dado de baja correctamente',
            'data': sector.json()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al dar de baja el sector: {str(e)}'
        }), 500
    finally:
        session.close()

