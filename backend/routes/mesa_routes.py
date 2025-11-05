from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Mesa, Sector

mesa_bp = Blueprint('mesa', __name__)

@mesa_bp.route('/', methods=['GET'])
def listar_mesas():
    session = SessionLocal()
    try:
        # Obtener parámetros de filtro
        sector_id = request.args.get('sector_id', type=int)
        tipo = request.args.get('tipo', type=str)
        estado = request.args.get('estado', type=str)  # 'activa' o 'baja'
        ordenar_por = request.args.get('ordenar_por', default='numero', type=str)
        
        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        # Validar parámetros de paginación
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        query = session.query(Mesa)
        
        # Filtros
        if sector_id:
            query = query.filter_by(id_sector=sector_id)
        if tipo:
            query = query.filter_by(tipo=tipo)
        if estado == 'activa':
            query = query.filter_by(baja=False)
        elif estado == 'baja':
            query = query.filter_by(baja=True)
        else:
            # Por defecto solo mostrar activas
            query = query.filter_by(baja=False)
        
        # Ordenamiento
        if ordenar_por == 'numero':
            query = query.order_by(Mesa.numero)
        elif ordenar_por == 'sector':
            query = query.join(Sector).order_by(Sector.numero)
        
        # Contar total antes de paginar
        total = query.count()
        
        # Aplicar paginación
        offset = (page - 1) * per_page
        mesas = query.offset(offset).limit(per_page).all()
        data = [m.json() for m in mesas]
        
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
            'message': f'Error al listar mesas: {str(e)}'
        }), 500
    finally:
        session.close()


@mesa_bp.route('/disponibles', methods=['GET'])
def listar_mesas_disponibles():
    session = SessionLocal()
    try:
        # Obtener parámetros de filtro
        cant_comensales = request.args.get('cant_comensales', type=int)
        sector_id = request.args.get('sector_id', type=int)
        
        query = session.query(Mesa).filter_by(baja=False)
        
        # Filtros
        if cant_comensales:
            query = query.filter(Mesa.cant_comensales >= cant_comensales)
        if sector_id:
            query = query.filter_by(id_sector=sector_id)
        
        # TODO: Filtrar mesas ocupadas o reservadas cuando existan esos modelos
        # Por ahora solo filtramos por baja=False
        
        mesas = query.all()
        data = [m.json() for m in mesas]
        
        return jsonify({
            'status': 'success',
            'data': data
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al listar mesas disponibles: {str(e)}'
        }), 500
    finally:
        session.close()


@mesa_bp.route('/tipos', methods=['GET'])
def listar_tipos_mesas():
    """Endpoint para obtener los tipos únicos de mesas"""
    session = SessionLocal()
    try:
        # Obtener tipos únicos de mesas activas
        tipos = session.query(Mesa.tipo).filter_by(baja=False).distinct().order_by(Mesa.tipo).all()
        tipos_list = [tipo[0] for tipo in tipos]
        
        return jsonify({
            'status': 'success',
            'data': tipos_list
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al listar tipos de mesas: {str(e)}'
        }), 500
    finally:
        session.close()


@mesa_bp.route('/', methods=['POST'])
def crear_mesa():
    session = SessionLocal()
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
        
        # Validar campos requeridos
        campos_requeridos = ['numero', 'tipo', 'cant_comensales', 'id_sector']
        for campo in campos_requeridos:
            if campo not in data or data[campo] is None:
                return jsonify({
                    'status': 'error',
                    'message': f'El campo "{campo}" es requerido'
                }), 400
        
        # Validar tipos de datos
        if not isinstance(data['cant_comensales'], int) or data['cant_comensales'] <= 0:
            return jsonify({
                'status': 'error',
                'message': 'La cantidad de comensales debe ser un número entero positivo'
            }), 400
        
        # Validar que el sector existe y está activo
        sector = session.query(Sector).filter_by(id_sector=data['id_sector']).first()
        if not sector:
            return jsonify({
                'status': 'error',
                'message': 'El sector indicado no existe'
            }), 400
        
        if sector.baja:
            return jsonify({
                'status': 'error',
                'message': 'El sector indicado está dado de baja'
            }), 400
        
        # Validar duplicados: número de mesa o id_mesa
        if 'id_mesa' in data:
            mesa_existente = session.query(Mesa).filter_by(id_mesa=data['id_mesa']).first()
            if mesa_existente:
                return jsonify({
                    'status': 'error',
                    'message': 'Ya existe una mesa con ese ID'
                }), 400
        
        mesa_existente = session.query(Mesa).filter_by(numero=data['numero']).first()
        if mesa_existente:
            return jsonify({
                'status': 'error',
                'message': 'Ya existe una mesa con ese número'
            }), 400
        
        # Crear mesa
        nueva_mesa = Mesa(
            numero=data['numero'],
            tipo=data['tipo'],
            cant_comensales=data['cant_comensales'],
            id_sector=data['id_sector'],
            baja=False
        )
        
        session.add(nueva_mesa)
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Mesa creada correctamente',
            'data': nueva_mesa.json()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al crear mesa: {str(e)}'
        }), 500
    finally:
        session.close()


@mesa_bp.route('/<int:id>', methods=['GET'])
def obtener_mesa(id):
    session = SessionLocal()
    try:
        mesa = session.query(Mesa).get(id)
        
        if not mesa:
            return jsonify({
                'status': 'error',
                'message': 'Mesa no encontrada'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': mesa.json()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener mesa: {str(e)}'
        }), 500
    finally:
        session.close()


@mesa_bp.route('/<int:id>', methods=['PUT'])
def modificar_mesa(id):
    session = SessionLocal()
    try:
        data = request.get_json()
        mesa = session.query(Mesa).get(id)
        
        if not mesa:
            return jsonify({
                'status': 'error',
                'message': 'Mesa no encontrada'
            }), 404
        
        if mesa.baja:
            return jsonify({
                'status': 'error',
                'message': 'No se puede modificar una mesa dada de baja'
            }), 400
        
        # TODO: Validar que la mesa no esté ocupada cuando exista el modelo de comanda
        # Por ahora solo validamos que no esté dada de baja
        
        # Validar cambios en campos
        if 'numero' in data:
            # Verificar que el nuevo número no esté duplicado
            mesa_duplicada = session.query(Mesa).filter_by(numero=data['numero']).first()
            if mesa_duplicada and mesa_duplicada.id_mesa != id:
                return jsonify({
                    'status': 'error',
                    'message': 'Ya existe otra mesa con ese número'
                }), 400
            mesa.numero = data['numero']
        
        if 'tipo' in data:
            mesa.tipo = data['tipo']
        
        if 'cant_comensales' in data:
            if not isinstance(data['cant_comensales'], int) or data['cant_comensales'] <= 0:
                return jsonify({
                    'status': 'error',
                    'message': 'La cantidad de comensales debe ser un número entero positivo'
                }), 400
            mesa.cant_comensales = data['cant_comensales']
        
        if 'id_sector' in data:
            # Validar que el nuevo sector existe y está activo
            nuevo_sector = session.query(Sector).filter_by(id_sector=data['id_sector']).first()
            if not nuevo_sector:
                return jsonify({
                    'status': 'error',
                    'message': 'El sector indicado no existe'
                }), 400
            
            if nuevo_sector.baja:
                return jsonify({
                    'status': 'error',
                    'message': 'El sector indicado está dado de baja'
                }), 400
            
            mesa.id_sector = data['id_sector']
        
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Mesa modificada correctamente',
            'data': mesa.json()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al modificar mesa: {str(e)}'
        }), 500
    finally:
        session.close()


@mesa_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_mesa(id):
    session = SessionLocal()
    try:
        mesa = session.query(Mesa).get(id)
        
        if not mesa:
            return jsonify({
                'status': 'error',
                'message': 'Mesa no encontrada'
            }), 404
        
        if mesa.baja:
            return jsonify({
                'status': 'error',
                'message': 'La mesa ya está dada de baja'
            }), 400
        
        # TODO: Validar que la mesa no esté asignada a una comanda activa o reserva vigente
        # Por ahora solo hacemos la baja lógica
        # Cuando existan los modelos de Comanda y Reserva, agregar validaciones:
        # - No se puede dar de baja si tiene comanda activa
        # - No se puede dar de baja si tiene reserva vigente
        
        mesa.baja = True
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Mesa dada de baja correctamente',
            'data': mesa.json()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al dar de baja la mesa: {str(e)}'
        }), 500
    finally:
        session.close()

