from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Cliente

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/', methods=['GET'])
def listar_clientes():
    """
    Lista todos los clientes con filtros y paginación.
    Filtros: documento, nombre, apellido, estado
    """
    session = SessionLocal()
    try:
        # --- Parámetros de Filtro para Cliente ---
        documento = request.args.get('documento', type=str)
        nombre = request.args.get('nombre', type=str)
        apellido = request.args.get('apellido', type=str)
        estado = request.args.get('estado', type=str)  # 'activa' o 'baja'
        ordenar_por = request.args.get('ordenar_por', default='apellido', type=str)
        
        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        # Validar parámetros de paginación
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        query = session.query(Cliente)
        
        # --- Filtros ---
        if documento:
            # Usamos 'like' para búsquedas parciales
            query = query.filter(Cliente.documento.like(f"%{documento}%"))
        if nombre:
            query = query.filter(Cliente.nombre.like(f"%{nombre}%"))
        if apellido:
            query = query.filter(Cliente.apellido.like(f"%{apellido}%"))
            
        if estado == 'activa':
            query = query.filter_by(baja=False)
        elif estado == 'baja':
            query = query.filter_by(baja=True)
        else:
            # Por defecto solo mostrar clientes activos
            query = query.filter_by(baja=False)
        
        # --- Ordenamiento ---
        if ordenar_por == 'documento':
            query = query.order_by(Cliente.documento)
        elif ordenar_por == 'nombre':
            query = query.order_by(Cliente.nombre)
        else:
            # Default
            query = query.order_by(Cliente.apellido)
        
        # Contar total antes de paginar
        total = query.count()
        
        # Aplicar paginación
        offset = (page - 1) * per_page
        clientes = query.offset(offset).limit(per_page).all()
        data = [c.json() for c in clientes]
        
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
            'message': f'Error al listar clientes: {str(e)}'
        }), 500
    finally:
        session.close()


@cliente_bp.route('/', methods=['POST'])
def crear_cliente():
    """Crea un nuevo cliente en la base de datos."""
    session = SessionLocal()
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
        
        # --- Validar campos requeridos para Cliente ---
        campos_requeridos = ['documento', 'nombre', 'apellido', 'num_telefono', 'email']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                return jsonify({
                    'status': 'error',
                    'message': f'El campo "{campo}" es requerido'
                }), 400
        
        # --- Validar duplicados (documento) ---
        cliente_existente = session.query(Cliente).filter_by(documento=data['documento']).first()
        if cliente_existente:
            return jsonify({
                'status': 'error',
                'message': 'Ya existe un cliente con ese documento'
            }), 400
        
        # Crear cliente
        nuevo_cliente = Cliente(
            documento=data['documento'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            num_telefono=data['num_telefono'],
            email=data['email'],
            baja=False
        )
        
        session.add(nuevo_cliente)
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Cliente creado correctamente',
            'data': nuevo_cliente.json()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al crear cliente: {str(e)}'
        }), 500
    finally:
        session.close()


@cliente_bp.route('/<int:id>', methods=['GET'])
def obtener_cliente(id):
    """Obtiene un cliente específico por su ID."""
    session = SessionLocal()
    try:
        cliente = session.query(Cliente).get(id)
        
        if not cliente:
            return jsonify({
                'status': 'error',
                'message': 'Cliente no encontrado'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': cliente.json()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener cliente: {str(e)}'
        }), 500
    finally:
        session.close()


@cliente_bp.route('/<int:id>', methods=['PUT'])
def modificar_cliente(id):
    """Modifica un cliente existente."""
    session = SessionLocal()
    try:
        data = request.get_json()
        cliente = session.query(Cliente).get(id)
        
        if not cliente:
            return jsonify({
                'status': 'error',
                'message': 'Cliente no encontrado'
            }), 404
        
        if cliente.baja:
            return jsonify({
                'status': 'error',
                'message': 'No se puede modificar un cliente dado de baja'
            }), 400
        
        # --- Validar cambios en campos de Cliente ---
        if 'documento' in data:
            # Verificar que el nuevo documento no esté duplicado
            cliente_duplicado = session.query(Cliente).filter_by(documento=data['documento']).first()
            if cliente_duplicado and cliente_duplicado.id_cliente != id:
                return jsonify({
                    'status': 'error',
                    'message': 'Ya existe otro cliente con ese documento'
                }), 400
            cliente.documento = data['documento']
        
        if 'nombre' in data:
            cliente.nombre = data['nombre']
        
        if 'apellido' in data:
            cliente.apellido = data['apellido']
        
        if 'num_telefono' in data:
            cliente.num_telefono = data['num_telefono']
            
        if 'email' in data:
            cliente.email = data['email']
        
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Cliente modificado correctamente',
            'data': cliente.json()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al modificar cliente: {str(e)}'
        }), 500
    finally:
        session.close()


@cliente_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    """Realiza una baja lógica de un cliente."""
    session = SessionLocal()
    try:
        cliente = session.query(Cliente).get(id)
        
        if not cliente:
            return jsonify({
                'status': 'error',
                'message': 'Cliente no encontrado'
            }), 404
        
        if cliente.baja:
            return jsonify({
                'status': 'error',
                'message': 'El cliente ya está dado de baja'
            }), 400
        
        # TODO: Validar que el cliente no tenga comandas activas o reservas
        
        cliente.baja = True
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Cliente dado de baja correctamente',
            'data': cliente.json()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error al dar de baja el cliente: {str(e)}'
        }), 500
    finally:
        session.close()