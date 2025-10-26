from flask import Blueprint, jsonify, request
from db import SessionLocal
from models.models import Producto, Seccion

producto_bp = Blueprint('producto', __name__)

@producto_bp.route('/', methods=['GET'])
def listar_productos():
    session = SessionLocal()
    productos = session.query(Producto).filter_by(baja=False).all()
    data = [p.json() for p in productos]
    session.close()
    return jsonify({
        'status': 'success',
        'data': data
    }), 200


@producto_bp.route('/', methods=['POST'])
def crear_producto():
    session = SessionLocal()
    data = request.get_json()

    campos_requeridos = ['codigo', 'nombre', 'precio', 'id_seccion']
    for campo in campos_requeridos:
        if campo not in data:
            session.close()
            return jsonify({
                'status': 'error',
                'message': f'El campo "{campo}" es requerido'
            }), 200

    seccion = session.query(Seccion).get(data['id_seccion'])
    if not seccion or seccion.baja:
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'La sección indicada no existe o está dada de baja'
        }), 200

    if session.query(Producto).filter_by(codigo=data['codigo']).first():
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'El código de producto ya existe'
        }), 200
    nuevo = Producto(
        codigo=data['codigo'],
        nombre=data['nombre'],
        precio=data['precio'],
        id_seccion=data['id_seccion'],
        descripcion=data.get('descripcion', None),
        baja=False
    )
    session.add(nuevo)
    session.commit()
    res = nuevo.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Producto creado correctamente',
        'data': res
    }), 200


@producto_bp.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    session = SessionLocal()
    producto = session.query(Producto).get(id)
    session.close()

    if not producto or producto.baja:
        return jsonify({
            'status': 'error',
            'message': 'Producto no encontrado'
        }), 200

    return jsonify({
        'status': 'success',
        'data': producto.json()
    }), 200

@producto_bp.route('/<int:id>', methods=['PUT'])
def editar_producto(id):
    session = SessionLocal()
    data = request.get_json()
    producto = session.query(Producto).get(id)

    if not producto or producto.baja:
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Producto no encontrado o dado de baja'
        }), 200

    for campo in ['codigo', 'nombre', 'precio', 'id_seccion', 'descripcion']:
        if campo in data:
            setattr(producto, campo, data[campo])
    session.commit()
    res = producto.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Producto actualizado correctamente',
        'data': res
    }), 200


@producto_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    session = SessionLocal()
    producto = session.query(Producto).get(id)

    if not producto or producto.baja:
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Producto no encontrado o ya dado de baja'
        }), 200

    producto.baja = True
    session.commit()
    res = producto.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Producto dado de baja correctamente',
        'data': res
    }), 200
