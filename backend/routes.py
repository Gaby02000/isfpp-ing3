from flask import Blueprint, Flask, jsonify, request
from db import SessionLocal
from models.models import Seccion, Producto, Plato, Postre, Bebida

api_bp = Blueprint('api', __name__)
@api_bp.route('/secciones', methods=['GET'])
def listar_secciones():
    session = SessionLocal()
    secciones = session.query(Seccion).all()
    data = [s.json() for s in secciones]
    session.close()
    return jsonify(data)


@api_bp.route('/secciones', methods=['POST'])
def crear_seccion():
    session = SessionLocal()
    data = request.get_json()
    nueva = Seccion(nombre=data['nombre'])
    session.add(nueva)
    session.commit()
    res = nueva.json()
    session.close()
    return jsonify(res), 201


@api_bp.route('/secciones/<int:id>', methods=['GET'])
def obtener_seccion(id):
    session = SessionLocal()
    seccion = session.query(Seccion).get(id)
    session.close()
    if not seccion:
        return jsonify({'error': 'Sección no encontrada'}), 404
    return jsonify(seccion.json())


@api_bp.route('/secciones/<int:id>', methods=['DELETE'])
def eliminar_seccion(id):
    session = SessionLocal()
    seccion = session.query(Seccion).get(id)
    if not seccion:
        session.close()
        return jsonify({'error': 'Sección no encontrada'}), 404
    session.delete(seccion)
    session.commit()
    session.close()
    return jsonify({'message': 'Sección eliminada correctamente'})

