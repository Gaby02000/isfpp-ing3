from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Comanda, Mesa, Mozo, Cliente, Producto, DetalleComanda
from datetime import datetime

comanda_bp = Blueprint('comanda', __name__)

@comanda_bp.route('/', methods=['GET'])
def listar_comandas():
    session = SessionLocal()
    try:
        # Obtener parámetros de filtro
        id_mozo = request.args.get('id_mozo', type=int)
        id_mesa = request.args.get('id_mesa', type=int)
        fecha = request.args.get('fecha', type=str)
        estado = request.args.get('estado', type=str)  # 'abierta', 'cerrada', 'cancelada', 'activa', 'baja'
        ordenar_por = request.args.get('ordenar_por', default='fecha', type=str)

        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Validar parámetros de paginación
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10

        query = session.query(Comanda)

        # Filtros
        if id_mozo:
            query = query.filter_by(id_mozo=id_mozo)
        if id_mesa:
            query = query.filter_by(id_mesa=id_mesa)
        if fecha:
            query = query.filter_by(fecha=fecha)
        
        # Filtros de estado
        if estado == 'abierta':
            query = query.filter_by(estado='Abierta', baja=False)
        elif estado == 'cerrada':
            query = query.filter_by(estado='Cerrada', baja=False)
        elif estado == 'cancelada':
            query = query.filter_by(estado='Cancelada', baja=False)
        elif estado == 'activa':
            query = query.filter_by(baja=False)
        elif estado == 'baja':
            query = query.filter_by(baja=True)
        else:
            # Por defecto solo mostrar activas (no dadas de baja)
            query = query.filter_by(baja=False)
        
        # Ordenamiento
        if ordenar_por == 'fecha':
            query = query.order_by(Comanda.fecha.desc())
        elif ordenar_por == 'fecha_asc':
            query = query.order_by(Comanda.fecha)
        elif ordenar_por == 'id_mozo':
            query = query.order_by(Comanda.id_mozo)
        elif ordenar_por == 'estado':
            query = query.order_by(Comanda.estado)

        # Contar total antes de paginar
        total = query.count()

        # Aplicar paginación
        offset = (page - 1) * per_page
        comandas = query.offset(offset).limit(per_page).all()
        data = [c.json() for c in comandas]

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
        return jsonify({'status':'error', 'message': f'Error al listar las comandas: {str(e)}'}), 500
    finally:
        session.close()

@comanda_bp.route('/abiertas', methods=['GET'])
def listar_comandas_abiertas():
    """Lista solo las comandas abiertas (estado='Abierta' y baja=False)"""
    session = SessionLocal()
    try:
        comandas = session.query(Comanda).filter_by(estado='Abierta', baja=False).all()
        data = [c.json() for c in comandas]
        return jsonify({
            'status': 'success',
            'data': data
        }), 200
    except Exception as e:
        return jsonify({'status':'error', 'message': f'Error al listar comandas abiertas: {str(e)}'}), 500
    finally:
        session.close()

@comanda_bp.route('/', methods=['POST'])
def create_comanda():
    session = SessionLocal()
    try:
        data = request.get_json()

        if not data:
            return jsonify({'status':'error', 'message': 'No se proporcionaron datos'}), 400
        
        # Validar campos obligatorios
            campos_requeridos = ['fecha', 'id_mozo', 'id_mesa']
        if 'fecha' not in data or data['fecha'] is None or data['fecha'] == '':
            return jsonify({'status':'error', 'message': f'El campo "fecha" es requerido'}), 400
        
        # Validar que la mesa no tenga una comanda abierta
        comanda_abierta = session.query(Comanda).filter_by(
            id_mesa=data['id_mesa'],
            estado='Abierta',
            baja=False
        ).first()
        if comanda_abierta:
            return jsonify({
                'status':'error',
                'message': f'La mesa {data["id_mesa"]} ya tiene una comanda abierta (id_comanda: {comanda_abierta.id_comanda})'
            }), 400
        
        # Validar cliente si se proporciona
        id_cliente = data.get('id_cliente')
        if id_cliente:
            cliente = session.query(Cliente).filter_by(id_cliente=id_cliente, baja=False).first()
            if not cliente:
                return jsonify({'status':'error', 'message': f'No existe un cliente activo con id_cliente {id_cliente}'}), 400
            
        # Crear comanda
        nueva_comanda = Comanda(
            fecha=data['fecha'],
            id_mozo=data['id_mozo'],
            id_mesa=data['id_mesa'],
            id_cliente=id_cliente,
            estado='Abierta',
            observaciones=data.get('observaciones')
        )
        session.add(nueva_comanda)
        session.flush()  # Para obtener el id_comanda
        
        # Agregar productos si se proporcionan
        productos = data.get('productos', [])
        if productos:
            for producto_data in productos:
                id_producto = producto_data.get('id_producto')
                cantidad = producto_data.get('cantidad', 1)
                
                if not id_producto or cantidad <= 0:
                    continue
                
                # Validar que el producto existe y está activo
                producto = session.query(Producto).filter_by(id_producto=id_producto, baja=False).first()
                if not producto:
                    continue
                
                # Crear detalle de comanda
                detalle = DetalleComanda(
                    id_comanda=nueva_comanda.id_comanda,
                    id_producto=id_producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                    entregado=False
                )
                session.add(detalle)
        
        session.commit()

        return jsonify({
            'status':'success',
            'message': 'Comanda creada exitosamente',
            'data': nueva_comanda.json()
        }), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al crear la comanda: {str(e)}'}), 500
    finally:
        session.close()

@comanda_bp.route('/<int:id_comanda>', methods=['GET'])
def obtener_comanda(id_comanda):
    session = SessionLocal()
    try:
        comanda = session.query(Comanda).filter_by(id_comanda=id_comanda).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id_comanda}'}), 404
        
        return jsonify({
            'status':'success',
            'data': comanda.json()
        }), 200
    except Exception as e:
        return jsonify({'status':'error', 'message': f'Error al obtener la comanda: {str(e)}'}), 500
    finally:
        session.close()

@comanda_bp.route('/<int:id>', methods=['PUT'])
def modificar_comanda(id):
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status':'error', 'message': 'No se proporcionaron datos'}), 400
        
        comanda = session.query(Comanda).filter_by(id_comanda=id).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id}'}), 404
        
        # Solo se pueden modificar comandas abiertas
        if comanda.estado != 'Abierta':
            return jsonify({
                'status':'error',
                'message': f'No se puede modificar una comanda con estado "{comanda.estado}". Solo se pueden modificar comandas abiertas.'
            }), 400
        
        # Actualizar campos permitidos
        if 'fecha' in data:
            comanda.fecha = data['fecha']

        if 'id_mozo' in data:
            # CORREGIDO: usar 'id' en lugar de 'id_mozo'
            nuevo_mozo = session.query(Mozo).filter_by(id=data['id_mozo']).first()
            if not nuevo_mozo:
                return jsonify({'status':'error', 'message': f'No existe un mozo con id {data["id_mozo"]}'}), 400
            if nuevo_mozo.baja:
                return jsonify({'status':'error', 'message': f'El mozo con id {data["id_mozo"]} está dado de baja'}), 400
            comanda.id_mozo = data['id_mozo']

        if 'id_mesa' in data:
            nueva_mesa = session.query(Mesa).filter_by(id_mesa=data['id_mesa']).first()
            if not nueva_mesa:
                return jsonify({'status':'error', 'message': f'No existe una mesa con id_mesa {data["id_mesa"]}'}), 400
            if nueva_mesa.baja:
                return jsonify({'status':'error', 'message': f'La mesa con id_mesa {data["id_mesa"]} está dada de baja'}), 400
            
            # Validar que la nueva mesa no tenga otra comanda abierta (si cambió de mesa)
            if data['id_mesa'] != comanda.id_mesa:
                comanda_abierta = session.query(Comanda).filter_by(
                    id_mesa=data['id_mesa'],
                    estado='Abierta',
                    baja=False
                ).first()
                if comanda_abierta and comanda_abierta.id_comanda != id:
                    return jsonify({
                        'status':'error',
                        'message': f'La mesa {data["id_mesa"]} ya tiene una comanda abierta'
                    }), 400
            
            comanda.id_mesa = data['id_mesa']
        
        if 'id_cliente' in data:
            if data['id_cliente'] is None:
                comanda.id_cliente = None
            else:
                cliente = session.query(Cliente).filter_by(id_cliente=data['id_cliente'], baja=False).first()
                if not cliente:
                    return jsonify({'status':'error', 'message': f'No existe un cliente activo con id_cliente {data["id_cliente"]}'}), 400
                comanda.id_cliente = data['id_cliente']
        
        if 'observaciones' in data:
            comanda.observaciones = data['observaciones']
        
        session.commit()
        return jsonify({
            'status':'success',
            'message': 'Comanda modificada exitosamente',
            'data': comanda.json()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al modificar la comanda: {str(e)}'}), 500
    finally:
        session.close()

@comanda_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_comanda(id):
    session = SessionLocal()
    try:
        comanda = session.query(Comanda).filter_by(id_comanda=id).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id}'}), 404
        
        if comanda.baja:
            return jsonify({'status':'error', 'message': f'La comanda con id_comanda {id} ya está dada de baja'}), 400
        
        # Cambiar estado a Cancelada en lugar de baja lógica
        if comanda.estado == 'Abierta':
            comanda.estado = 'Cancelada'
        comanda.baja = True
        session.commit()
        return jsonify({
            'status':'success',
            'message': 'Comanda cancelada exitosamente',
            'data': comanda.json()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al cancelar la comanda: {str(e)}'}), 500
    finally:
        session.close()

# ========== RUTAS PARA GESTIÓN DE PRODUCTOS ==========

@comanda_bp.route('/<int:id_comanda>/productos', methods=['POST'])
def agregar_producto_comanda(id_comanda):
    """Agregar un producto a una comanda abierta"""
    session = SessionLocal()
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status':'error', 'message': 'No se proporcionaron datos'}), 400
        
        # Validar campos requeridos
        if 'id_producto' not in data or 'cantidad' not in data:
            return jsonify({'status':'error', 'message': 'Los campos "id_producto" y "cantidad" son requeridos'}), 400
        
        id_producto = data['id_producto']
        cantidad = data['cantidad']
        
        if not isinstance(cantidad, int) or cantidad <= 0:
            return jsonify({'status':'error', 'message': 'La cantidad debe ser un número entero positivo'}), 400
        
        # Validar que la comanda existe y está abierta
        comanda = session.query(Comanda).filter_by(id_comanda=id_comanda).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id_comanda}'}), 404
        
        if comanda.estado != 'Abierta':
            return jsonify({
                'status':'error',
                'message': f'No se pueden agregar productos a una comanda con estado "{comanda.estado}". Solo se pueden agregar productos a comandas abiertas.'
            }), 400
        
        # Validar que el producto existe y está activo
        producto = session.query(Producto).filter_by(id_producto=id_producto, baja=False).first()
        if not producto:
            return jsonify({'status':'error', 'message': f'No existe un producto activo con id_producto {id_producto}'}), 400
        
        # Crear detalle de comanda
        detalle = DetalleComanda(
            id_comanda=id_comanda,
            id_producto=id_producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            entregado=False
        )
        session.add(detalle)
        session.commit()
        
        return jsonify({
            'status':'success',
            'message': 'Producto agregado a la comanda exitosamente',
            'data': detalle.json()
        }), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al agregar producto a la comanda: {str(e)}'}), 500
    finally:
        session.close()

@comanda_bp.route('/<int:id_comanda>/productos/<int:id_detalle>', methods=['PUT'])
def modificar_cantidad_producto(id_comanda, id_detalle):
    """Modificar la cantidad de un producto en una comanda abierta"""
    session = SessionLocal()
    try:
        data = request.get_json()
        
        if 'cantidad' not in data:
            return jsonify({'status':'error', 'message': 'El campo "cantidad" es requerido'}), 400
        
        cantidad = data['cantidad']
        if not isinstance(cantidad, int) or cantidad <= 0:
            return jsonify({'status':'error', 'message': 'La cantidad debe ser un número entero positivo'}), 400
        
        # Validar que la comanda existe y está abierta
        comanda = session.query(Comanda).filter_by(id_comanda=id_comanda).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id_comanda}'}), 404
        
        if comanda.estado != 'Abierta':
            return jsonify({
                'status':'error',
                'message': f'No se pueden modificar productos de una comanda con estado "{comanda.estado}". Solo se pueden modificar comandas abiertas.'
            }), 400
        
        # Validar que el detalle existe y pertenece a la comanda
        detalle = session.query(DetalleComanda).filter_by(
            id_detalle_comanda=id_detalle,
            id_comanda=id_comanda
        ).first()
        
        if not detalle:
            return jsonify({
                'status':'error',
                'message': f'No existe un detalle con id_detalle_comanda {id_detalle} en la comanda {id_comanda}'
            }), 404
        
        detalle.cantidad = cantidad
        session.commit()
        
        return jsonify({
            'status':'success',
            'message': 'Cantidad modificada exitosamente',
            'data': detalle.json()
        }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al modificar cantidad: {str(e)}'}), 500
    finally:
        session.close()

@comanda_bp.route('/<int:id_comanda>/productos/<int:id_detalle>', methods=['DELETE'])
def eliminar_producto_comanda(id_comanda, id_detalle):
    """Eliminar un producto de una comanda abierta"""
    session = SessionLocal()
    try:
        # Validar que la comanda existe y está abierta
        comanda = session.query(Comanda).filter_by(id_comanda=id_comanda).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id_comanda}'}), 404
        
        if comanda.estado != 'Abierta':
            return jsonify({
                'status':'error',
                'message': f'No se pueden eliminar productos de una comanda con estado "{comanda.estado}". Solo se pueden eliminar productos de comandas abiertas.'
            }), 400
        
        # Validar que el detalle existe y pertenece a la comanda
        detalle = session.query(DetalleComanda).filter_by(
            id_detalle_comanda=id_detalle,
            id_comanda=id_comanda
        ).first()
        
        if not detalle:
            return jsonify({
                'status':'error',
                'message': f'No existe un detalle con id_detalle_comanda {id_detalle} en la comanda {id_comanda}'
            }), 404
        
        session.delete(detalle)
        session.commit()
        
        return jsonify({
            'status':'success',
            'message': 'Producto eliminado de la comanda exitosamente'
        }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al eliminar producto de la comanda: {str(e)}'}), 500
    finally:
        session.close()

@comanda_bp.route('/<int:id_comanda>/productos/<int:id_detalle>/entregar', methods=['POST'])
def entregar_producto(id_comanda, id_detalle):
    """Marcar un producto como entregado en una comanda abierta"""
    session = SessionLocal()
    try:
        # Validar que la comanda existe y está abierta
        comanda = session.query(Comanda).filter_by(id_comanda=id_comanda).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id_comanda}'}), 404
        
        if comanda.estado != 'Abierta':
            return jsonify({
                'status':'error',
                'message': f'No se pueden marcar productos como entregados en una comanda con estado "{comanda.estado}". Solo se pueden marcar en comandas abiertas.'
            }), 400
        
        # Validar que el detalle existe y pertenece a la comanda
        detalle = session.query(DetalleComanda).filter_by(
            id_detalle_comanda=id_detalle,
            id_comanda=id_comanda
        ).first()
        
        if not detalle:
            return jsonify({
                'status':'error',
                'message': f'No existe un detalle con id_detalle_comanda {id_detalle} en la comanda {id_comanda}'
            }), 404
        
        detalle.entregado = True
        session.commit()
        
        return jsonify({
            'status':'success',
            'message': 'Producto marcado como entregado exitosamente',
            'data': detalle.json()
        }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al marcar producto como entregado: {str(e)}'}), 500
    finally:
        session.close()

# ========== RUTA PARA CERRAR COMANDA ==========

@comanda_bp.route('/<int:id_comanda>/cerrar', methods=['POST'])
def cerrar_comanda(id_comanda):
    """Cerrar una comanda abierta (solo si todos los productos están entregados)"""
    session = SessionLocal()
    try:
        # Validar que la comanda existe
        comanda = session.query(Comanda).filter_by(id_comanda=id_comanda).first()
        if not comanda:
            return jsonify({'status':'error', 'message': f'No existe una comanda con id_comanda {id_comanda}'}), 404
        
        if comanda.estado != 'Abierta':
            return jsonify({
                'status':'error',
                'message': f'No se puede cerrar una comanda con estado "{comanda.estado}". Solo se pueden cerrar comandas abiertas.'
            }), 400
        
        # Validar que todos los productos estén entregados
        detalles_no_entregados = session.query(DetalleComanda).filter_by(
            id_comanda=id_comanda,
            entregado=False
        ).count()
        
        if detalles_no_entregados > 0:
            return jsonify({
                'status':'error',
                'message': f'No se puede cerrar la comanda. Hay {detalles_no_entregados} producto(s) sin entregar.'
            }), 400
        
        # Cerrar la comanda
        comanda.estado = 'Cerrada'
        comanda.fecha_cierre = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session.commit()
        
        return jsonify({
            'status':'success',
            'message': 'Comanda cerrada exitosamente',
            'data': comanda.json()
        }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al cerrar la comanda: {str(e)}'}), 500
    finally:
        session.close()
