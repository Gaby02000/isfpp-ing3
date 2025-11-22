from flask import Blueprint, jsonify, request
from db import SessionLocal
from models.reserva import Reserva
from models import Cliente, Mesa
from datetime import datetime

reserva_bp = Blueprint('reserva_bp', __name__)

@reserva_bp.route('/', methods=['GET'])
def listar_reservas():
    session = SessionLocal()
    try:
        cancelado = request.args.get('cancelado', type=str)
        cliente_id = request.args.get('cliente_id', type=int)
        fecha_desde = request.args.get('fecha_desde', type=str)
        fecha_hasta = request.args.get('fecha_hasta', type=str)
        order_by = request.args.get('order_by', default='fecha_hora', type=str)
        
        # Paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        query = session.query(Reserva)
        
        # Filtros
        if cancelado:
            if cancelado.lower() == 'activo':
                query = query.filter_by(cancelado=False)
            elif cancelado.lower() == 'cancelado':
                query = query.filter_by(cancelado=True)
        if cliente_id:
            query = query.filter_by(id_cliente=cliente_id)

        # Filtro por rango de fecha
        if fecha_desde:
            try:
                fd = datetime.fromisoformat(fecha_desde)
                query = query.filter(Reserva.fecha_hora >= fd)
            except Exception:
                return jsonify({'status': 'error', 'message': 'fecha_desde inválida, usar ISO format'}), 400
        if fecha_hasta:
            try:
                fh = datetime.fromisoformat(fecha_hasta)
                query = query.filter(Reserva.fecha_hora <= fh)
            except Exception:
                return jsonify({'status': 'error', 'message': 'fecha_hasta inválida, usar ISO format'}), 400

        # Orden
        if order_by == 'numero':
            query = query.order_by(Reserva.numero)
        else:
            query = query.order_by(Reserva.fecha_hora)
        
        # Total antes de paginar
        total = query.count()
        
        # Paginación
        offset = (page - 1) * per_page
        reservas = query.offset(offset).limit(per_page).all()
        
        data = []
        for r in reservas:
            item = r.json()
            # Derivar estado
            if not r.cancelado:
                estado = 'activa'
            else:
                if r.motivo_cancelacion and r.motivo_cancelacion.lower() == 'ausencia':
                    estado = 'por ausencia'
                else:
                    estado = 'cancelada'
            item['estado'] = estado
            data.append(item)
        
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
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

        
@reserva_bp.route('/', methods=['POST'])
def crear_reserva():
    session = SessionLocal()
    try:
        data = request.get_json()

        if not data:
            return jsonify({'status': 'error', 'message': 'No input data provided'}), 400

        # Campos requeridos
        campos_requeridos = ['numero', 'fecha_hora', 'cant_personas', 'id_cliente', 'id_mesa']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({'status': 'error', 'message': f'Campo {campo} es requerido'}), 400 
        
        fecha_reserva = datetime.fromisoformat(data['fecha_hora'])
        if fecha_reserva <= datetime.now():
            return jsonify({
                'status': 'error',
                'message': 'La fecha y hora de la reserva debe ser futura'
            }), 400

        # Validación de cliente
        cliente = session.query(Cliente).get(data['id_cliente'])
        if not cliente:
            return jsonify({'status': 'error', 'message': 'Cliente no encontrado'}), 404
        if cliente.baja:
            return jsonify({'status': 'error', 'message': 'Cliente dado de baja'}), 400
        
        # Validación de mesa
        mesa = session.query(Mesa).get(data['id_mesa'])
        if not mesa:
            return jsonify({'status': 'error', 'message': 'Mesa no encontrada'}), 404
        if mesa.baja:
            return jsonify({'status': 'error', 'message': 'Mesa dada de baja'}), 400
        if mesa.cant_comensales < data['cant_personas']:
            return jsonify({'status': 'error', 'message': 'Capacidad de mesa insuficiente'}), 400
        
        # Validación de disponibilidad de mesa
        reserva_existente = session.query(Reserva).filter_by(
            id_mesa=data['id_mesa'],
            fecha_hora=data['fecha_hora'],
            cancelado=False
        ).first()
        if reserva_existente:
            return jsonify({'status': 'error', 'message': 'La mesa ya está reservada para la fecha y hora seleccionadas'}), 400

        # Validación de duplicado de número
        reserva_numero = session.query(Reserva).filter_by(numero=data['numero']).first()
        if reserva_numero:
            return jsonify({'status': 'error', 'message': 'El número de reserva ya existe'}), 400
        
        # Crear reserva
        nueva_reserva = Reserva(
            numero=data['numero'],
            fecha_hora=data['fecha_hora'],
            cant_personas=data['cant_personas'],
            id_cliente=data['id_cliente'],
            id_mesa=data['id_mesa'],
            cancelado=False   # 👈 boolean correcto
        )
        session.add(nueva_reserva)
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Reserva creada exitosamente',
            'data': nueva_reserva.json()
        }), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

@reserva_bp.route('/<int:reserva_id>', methods=['GET'])
def obtener_reserva(reserva_id):   # 👈 corregido nombre del parámetro
    session = SessionLocal()
    try:
        reserva = session.query(Reserva).get(reserva_id)
        if not reserva:
            return jsonify({'status': 'error', 'message': 'Reserva no encontrada'}), 404

        return jsonify({'status': 'success', 'data': reserva.json()}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al obtener reserva: {str(e)}'}), 500
    finally:
        session.close()

@reserva_bp.route('/<int:id>/cancelar', methods=['PUT'])
def cancelar_reserva(id):
    session = SessionLocal()
    try:
        reserva = session.query(Reserva).get(id)
        if not reserva:
            return jsonify({'status': 'error', 'message': 'Reserva no encontrada'}), 404

        data = request.get_json() or {}
        motivo = data.get('motivo')
        if not motivo:
            return jsonify({'status': 'error', 'message': 'motivo es requerido para cancelar la reserva'}), 400

        reserva.cancelado = True
        reserva.motivo_cancelacion = motivo
        # Registrar si se devuelve la seña
        if 'senia_devuelta' in data:
            reserva.senia_devuelta = bool(data.get('senia_devuelta'))
        reserva.fecha_modificacion = datetime.now()
        session.commit()

        return jsonify({'status': 'success', 'message': 'Reserva cancelada correctamente', 'data': reserva.json()}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status': 'error', 'message': f'Error al cancelar reserva: {str(e)}'}), 500
    finally:
        session.close()

@reserva_bp.route('/<int:id>', methods=['PUT'])
def actualizar_reserva(id):
    session = SessionLocal()
    try:
        data = request.get_json()
        reserva = session.query(Reserva).get(id)
        if not reserva:
            return jsonify({'status': 'error', 'message': 'Reserva no encontrada'}), 404
        # No se puede modificar una reserva cancelada
        if reserva.cancelado:
            return jsonify({'status': 'error', 'message': 'No se puede modificar una reserva cancelada'}), 400

        # Campos a actualizar
        nueva_numero = data.get('numero', reserva.numero)
        nueva_fecha_raw = data.get('fecha_hora')
        nueva_cant = data.get('cant_personas', reserva.cant_personas)
        nuevo_cliente_id = data.get('id_cliente', reserva.id_cliente)
        nueva_mesa_id = data.get('id_mesa', reserva.id_mesa)

        # Validar fecha futura si se cambia
        if nueva_fecha_raw:
            try:
                nueva_fecha = datetime.fromisoformat(nueva_fecha_raw)
            except Exception:
                return jsonify({'status': 'error', 'message': 'fecha_hora inválida, usar ISO format'}), 400
            if nueva_fecha <= datetime.now():
                return jsonify({'status': 'error', 'message': 'La fecha y hora de la reserva debe ser futura'}), 400
        else:
            nueva_fecha = reserva.fecha_hora

        # Validar mesa y capacidad
        mesa = session.query(Mesa).get(nueva_mesa_id)
        if not mesa:
            return jsonify({'status': 'error', 'message': 'Mesa no encontrada'}), 404
        if mesa.baja:
            return jsonify({'status': 'error', 'message': 'Mesa dada de baja'}), 400
        if mesa.cant_comensales < nueva_cant:
            return jsonify({'status': 'error', 'message': 'Capacidad de mesa insuficiente'}), 400

        # Validar disponibilidad de mesa en la nueva fecha (excluir la propia reserva)
        conflicto = session.query(Reserva).filter(
            Reserva.id_mesa == nueva_mesa_id,
            Reserva.fecha_hora == nueva_fecha,
            Reserva.cancelado == False,
            Reserva.id_reserva != id
        ).first()
        if conflicto:
            return jsonify({'status': 'error', 'message': 'La mesa ya está reservada para la fecha y hora seleccionadas'}), 400

        # Aplicar cambios
        reserva.numero = nueva_numero
        reserva.fecha_hora = nueva_fecha
        reserva.cant_personas = nueva_cant
        reserva.id_cliente = nuevo_cliente_id
        reserva.id_mesa = nueva_mesa_id
        reserva.fecha_modificacion = datetime.now()

        session.commit()
        return jsonify({'status': 'success', 'message': 'Reserva actualizada', 'data': reserva.json()}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()


@reserva_bp.route('/<int:id>/ausencia', methods=['PUT'])
def ausencia_reserva(id):
    session = SessionLocal()
    try:
        reserva = session.query(Reserva).get(id)
        if not reserva:
            return jsonify({'status': 'error', 'message': 'Reserva no encontrada'}), 404

        # La hora de la reserva debe haber pasado
        if reserva.fecha_hora > datetime.now():
            return jsonify({'status': 'error', 'message': 'La reserva aún no ocurrió; no puede marcarse como ausencia'}), 400

        # No marcar ausencia si ya asistió
        if reserva.asistida:
            return jsonify({'status': 'error', 'message': 'Reserva ya marcada como asistida'}), 400

        data = request.get_json() or {}
        # Marcar ausencia
        reserva.cancelado = True
        reserva.motivo_cancelacion = 'ausencia'
        reserva.senia_recuperada = bool(data.get('senia_recuperada', True))
        reserva.fecha_modificacion = datetime.now()

        session.commit()
        return jsonify({'status': 'success', 'message': 'Reserva marcada como ausencia', 'data': reserva.json()}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status': 'error', 'message': f'Error al marcar ausencia: {str(e)}'}), 500
    finally:
        session.close()