from flask import Blueprint, jsonify, request
from db import SessionLocal
from models.models import Seccion

seccion_bp = Blueprint('seccion', __name__)

@seccion_bp.route('/', methods=['GET'])
def listar_secciones():
    session = SessionLocal()
    secciones = session.query(Seccion).filter_by(baja=False).all()
    data = [s.json() for s in secciones]
    session.close()
    return jsonify({
        'status': 'success',
        'data': data
    }), 200


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