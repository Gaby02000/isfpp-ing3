from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Mozo, Sector

mozo_bp = Blueprint('mozo', __name__)


@mozo_bp.route('/', methods=['GET'])
def listar_mozos():
    session = SessionLocal()
    activos = request.args.get('activos', '').lower() == 'true'
    if activos:
        mozos = session.query(Mozo).filter_by(baja=False).all()
    else:
        mozos = session.query(Mozo).all()

    data = [m.json() for m in mozos]
    session.close()
    return jsonify({'status': 'success', 'data': data}), 200


@mozo_bp.route('/<int:id>', methods=['GET'])
def obtener_mozo(id):
    session = SessionLocal()
    mozo = session.query(Mozo).get(id)
    session.close()

    if not mozo or mozo.baja:
        return jsonify({'status': 'error', 'message': 'Mozo no encontrado'}), 200

    return jsonify({'status': 'success', 'data': mozo.json()}), 200


@mozo_bp.route('/', methods=['POST'])
def crear_mozo():
    session = SessionLocal()
    data = request.get_json() or {}

    # Campos obligatorios: nombre_apellido y documento (sector ahora opcional)
    campos_requeridos = ['nombre_apellido', 'documento']
    for campo in campos_requeridos:
        if campo not in data:
            session.close()
            return jsonify({'status': 'error', 'message': f'El campo "{campo}" es requerido'}), 200

    # Si se provee id_sector, validar que el sector exista y no esté dado de baja
    if 'id_sector' in data and data.get('id_sector') is not None:
        sector = session.query(Sector).filter_by(id_sector=data['id_sector']).first()
        if not sector or sector.baja:
            session.close()
            return jsonify({'status': 'error', 'message': 'El sector indicado no existe o está dado de baja'}), 200

    # Documento único
    if session.query(Mozo).filter_by(documento=data['documento']).first():
        session.close()
        return jsonify({'status': 'error', 'message': 'El documento ya existe'}), 200

    nuevo = Mozo(
        documento=data['documento'],
        nombre_apellido=data['nombre_apellido'],
        id_sector=data.get('id_sector'),
        direccion=data.get('direccion'),
        telefono=data.get('telefono'),
        baja=False
    )
    session.add(nuevo)
    session.commit()
    res = nuevo.json()
    session.close()

    return jsonify({'status': 'success', 'message': 'Mozo creado correctamente', 'data': res}), 200


@mozo_bp.route('/<int:id>', methods=['PUT'])
def actualizar_mozo(id):
    session = SessionLocal()
    data = request.get_json() or {}
    mozo = session.query(Mozo).get(id)

    if not mozo or mozo.baja:
        session.close()
        return jsonify({'status': 'error', 'message': 'Mozo no encontrado o dado de baja'}), 200

    # Si se intenta cambiar documento, validar unicidad
    if 'documento' in data and data['documento'] != mozo.documento:
        if session.query(Mozo).filter_by(documento=data['documento']).first():
            session.close()
            return jsonify({'status': 'error', 'message': 'El documento ya existe'}), 200

    # Si se actualiza sector y no es null, validar existencia; si es null se permite quitar el sector
    if 'id_sector' in data and data.get('id_sector') is not None:
        # El modelo Sector tiene la columna 'id', validar por esa columna
        sector = session.query(Sector).filter_by(id_sector=data['id_sector']).first()
        if not sector or sector.baja:
            session.close()
            return jsonify({'status': 'error', 'message': 'El sector indicado no existe o está dado de baja'}), 200

    # Campos editables
    for campo in ['documento', 'nombre_apellido', 'direccion', 'telefono', 'id_sector']:
        if campo in data:
            setattr(mozo, campo, data[campo])

    session.commit()
    res = mozo.json()
    session.close()

    return jsonify({'status': 'success', 'message': 'Mozo actualizado correctamente', 'data': res}), 200


@mozo_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_mozo(id):
    session = SessionLocal()
    mozo = session.query(Mozo).get(id)

    if not mozo or mozo.baja:
        session.close()
        return jsonify({'status': 'error', 'message': 'Mozo no encontrado o ya dado de baja'}), 200

    mozo.baja = True
    session.commit()
    res = mozo.json()
    session.close()

    return jsonify({'status': 'success', 'message': 'Mozo dado de baja correctamente', 'data': res}), 200
