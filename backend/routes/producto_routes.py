from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Producto, Seccion, Plato, Postre, Bebida

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

    campos_requeridos = ['codigo', 'nombre', 'precio', 'id_seccion', 'tipo']
    for campo in campos_requeridos:
        if campo not in data:
            session.close()
            return jsonify({
                'status': 'error',
                'message': f'El campo "{campo}" es requerido'
            }), 200

    seccion = session.query(Seccion).filter_by(id_seccion=data['id_seccion']).first()
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
    
    if data['tipo'] == 'plato':
        nuevo = Plato(
            id_plato=data['id_plato'],
            producto=nuevo
        )
    elif data['tipo'] == 'postre':
        nuevo = Postre(
            id_postre=data['id_postre'],
            producto=nuevo
        )
    elif data['tipo'] == 'bebida':
        nuevo = Bebida(
            id_bebida=data['id_bebida'],
            producto=nuevo
        )
    else:
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'El tipo de producto no es válido'
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


# Rutas para Plato
@producto_bp.route('/platos', methods=['GET'])
def listar_platos():
    session = SessionLocal()
    platos = session.query(Plato).join(Producto).filter(Producto.baja == False).all()
    data = [p.json() for p in platos]
    session.close()
    return jsonify({
        'status': 'success',
        'data': data
    }), 200


@producto_bp.route('/platos', methods=['POST'])
def crear_plato():
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

    seccion = session.query(Seccion).filter_by(id_seccion=data['id_seccion']).first()
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

    producto = Producto(
        codigo=data['codigo'],
        nombre=data['nombre'],
        precio=data['precio'],
        id_seccion=data['id_seccion'],
        descripcion=data.get('descripcion', None),
        baja=False
    )
    session.add(producto)
    session.flush()

    plato = Plato(id_plato=producto.id_producto)
    session.add(plato)
    session.commit()
    res = plato.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Plato creado correctamente',
        'data': res
    }), 200


@producto_bp.route('/platos/<int:id>', methods=['GET'])
def obtener_plato(id):
    session = SessionLocal()
    plato = session.query(Plato).filter_by(id_plato=id).first()
    session.close()

    if not plato or (plato.producto and plato.producto.baja):
        return jsonify({
            'status': 'error',
            'message': 'Plato no encontrado'
        }), 200

    return jsonify({
        'status': 'success',
        'data': plato.json()
    }), 200


@producto_bp.route('/platos/<int:id>', methods=['PUT'])
def editar_plato(id):
    session = SessionLocal()
    data = request.get_json()
    plato = session.query(Plato).filter_by(id_plato=id).first()

    if not plato or (plato.producto and plato.producto.baja):
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Plato no encontrado o dado de baja'
        }), 200

    producto = plato.producto
    if producto:
        for campo in ['codigo', 'nombre', 'precio', 'id_seccion', 'descripcion']:
            if campo in data:
                setattr(producto, campo, data[campo])
    session.commit()
    res = plato.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Plato actualizado correctamente',
        'data': res
    }), 200


@producto_bp.route('/platos/<int:id>', methods=['DELETE'])
def eliminar_plato(id):
    session = SessionLocal()
    plato = session.query(Plato).filter_by(id_plato=id).first()

    if not plato or (plato.producto and plato.producto.baja):
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Plato no encontrado o ya dado de baja'
        }), 200

    if plato.producto:
        plato.producto.baja = True
    session.commit()
    res = plato.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Plato dado de baja correctamente',
        'data': res
    }), 200


# Rutas para Postre
@producto_bp.route('/postres', methods=['GET'])
def listar_postres():
    session = SessionLocal()
    postres = session.query(Postre).join(Producto).filter(Producto.baja == False).all()
    data = [p.json() for p in postres]
    session.close()
    return jsonify({
        'status': 'success',
        'data': data
    }), 200


@producto_bp.route('/postres', methods=['POST'])
def crear_postre():
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

    seccion = session.query(Seccion).filter_by(id_seccion=data['id_seccion']).first()
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

    producto = Producto(
        codigo=data['codigo'],
        nombre=data['nombre'],
        precio=data['precio'],
        id_seccion=data['id_seccion'],
        descripcion=data.get('descripcion', None),
        baja=False
    )
    session.add(producto)
    session.flush()

    postre = Postre(id_postre=producto.id_producto)
    session.add(postre)
    session.commit()
    res = postre.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Postre creado correctamente',
        'data': res
    }), 200


@producto_bp.route('/postres/<int:id>', methods=['GET'])
def obtener_postre(id):
    session = SessionLocal()
    postre = session.query(Postre).filter_by(id_postre=id).first()
    session.close()

    if not postre or (postre.producto and postre.producto.baja):
        return jsonify({
            'status': 'error',
            'message': 'Postre no encontrado'
        }), 200

    return jsonify({
        'status': 'success',
        'data': postre.json()
    }), 200


@producto_bp.route('/postres/<int:id>', methods=['PUT'])
def editar_postre(id):
    session = SessionLocal()
    data = request.get_json()
    postre = session.query(Postre).filter_by(id_postre=id).first()

    if not postre or (postre.producto and postre.producto.baja):
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Postre no encontrado o dado de baja'
        }), 200

    producto = postre.producto
    if producto:
        for campo in ['codigo', 'nombre', 'precio', 'id_seccion', 'descripcion']:
            if campo in data:
                setattr(producto, campo, data[campo])
    session.commit()
    res = postre.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Postre actualizado correctamente',
        'data': res
    }), 200


@producto_bp.route('/postres/<int:id>', methods=['DELETE'])
def eliminar_postre(id):
    session = SessionLocal()
    postre = session.query(Postre).filter_by(id_postre=id).first()

    if not postre or (postre.producto and postre.producto.baja):
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Postre no encontrado o ya dado de baja'
        }), 200

    if postre.producto:
        postre.producto.baja = True
    session.commit()
    res = postre.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Postre dado de baja correctamente',
        'data': res
    }), 200


# Rutas para Bebida
@producto_bp.route('/bebidas', methods=['GET'])
def listar_bebidas():
    session = SessionLocal()
    bebidas = session.query(Bebida).join(Producto).filter(Producto.baja == False).all()
    data = [b.json() for b in bebidas]
    session.close()
    return jsonify({
        'status': 'success',
        'data': data
    }), 200


@producto_bp.route('/bebidas', methods=['POST'])
def crear_bebida():
    session = SessionLocal()
    data = request.get_json()

    campos_requeridos = ['codigo', 'nombre', 'precio', 'id_seccion', 'cm3']
    for campo in campos_requeridos:
        if campo not in data:
            session.close()
            return jsonify({
                'status': 'error',
                'message': f'El campo "{campo}" es requerido'
            }), 200

    seccion = session.query(Seccion).filter_by(id_seccion=data['id_seccion']).first()
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

    producto = Producto(
        codigo=data['codigo'],
        nombre=data['nombre'],
        precio=data['precio'],
        id_seccion=data['id_seccion'],
        descripcion=data.get('descripcion', None),
        baja=False
    )
    session.add(producto)
    session.flush()

    bebida = Bebida(id_bebida=producto.id_producto, cm3=data['cm3'])
    session.add(bebida)
    session.commit()
    res = bebida.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Bebida creada correctamente',
        'data': res
    }), 200


@producto_bp.route('/bebidas/<int:id>', methods=['GET'])
def obtener_bebida(id):
    session = SessionLocal()
    bebida = session.query(Bebida).filter_by(id_bebida=id).first()
    session.close()

    if not bebida or (bebida.producto and bebida.producto.baja):
        return jsonify({
            'status': 'error',
            'message': 'Bebida no encontrada'
        }), 200

    return jsonify({
        'status': 'success',
        'data': bebida.json()
    }), 200


@producto_bp.route('/bebidas/<int:id>', methods=['PUT'])
def editar_bebida(id):
    session = SessionLocal()
    data = request.get_json()
    bebida = session.query(Bebida).filter_by(id_bebida=id).first()

    if not bebida or (bebida.producto and bebida.producto.baja):
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Bebida no encontrada o dada de baja'
        }), 200

    producto = bebida.producto
    if producto:
        for campo in ['codigo', 'nombre', 'precio', 'id_seccion', 'descripcion']:
            if campo in data:
                setattr(producto, campo, data[campo])
    
    if 'cm3' in data:
        bebida.cm3 = data['cm3']
    
    session.commit()
    res = bebida.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Bebida actualizada correctamente',
        'data': res
    }), 200


@producto_bp.route('/bebidas/<int:id>', methods=['DELETE'])
def eliminar_bebida(id):
    session = SessionLocal()
    bebida = session.query(Bebida).filter_by(id_bebida=id).first()

    if not bebida or (bebida.producto and bebida.producto.baja):
        session.close()
        return jsonify({
            'status': 'error',
            'message': 'Bebida no encontrada o ya dada de baja'
        }), 200

    if bebida.producto:
        bebida.producto.baja = True
    session.commit()
    res = bebida.json()
    session.close()

    return jsonify({
        'status': 'success',
        'message': 'Bebida dada de baja correctamente',
        'data': res
    }), 200
