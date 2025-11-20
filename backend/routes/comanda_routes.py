from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Comanda  

comanda_bp = Blueprint('comanda', __name__)

@mesa_bp.route('/', methods=['GET'])
def listar_comandas():
    session = SessionLocal()
    try:
        #obtener parametros de filtro
        id_mozo = request.args.get('id_mozo', type=int)
        id_mesa = request.args.get('id_mesa', type=int)
        fecha = request.args.get('fecha', type=str)
        estado = request.args.get('estado', type=str)  # 'activa' o 'baja' o 'cerrada'
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
        if estado == 'activa':
            query = query.filter_by(baja=False)
        elif estado == 'baja':
            query = query.filter_by(baja=True)
        elif estado == 'cerrada':
            query = query.filter_by(cerrado=True) #dudoso
        else:
            # Por defecto solo mostrar activas
            query = query.filter_by(baja=False)
        
        # Ordenamiento
        if ordenar_por == 'fecha':
            query = query.order_by(Comanda.fecha)
        elif ordenar_por == 'id_mozo':
            query = query.order_by(Comanda.id_mozo)

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
                'total_pages': total_pages
            }
        }), 200
    except Exception as e:
        return jsonify({'status':'error', 'message': f'Error al listar las comandas: {str(e)}'}), 500
    finally:
        session.close()

#Listar comandas abiertas??

@comanda_bp.route('/', methods=['POST'])
def create_comanda():
    session = SessionLocal()
    try:
        data = request.get_json()

        if not data:
            return jsonify({'status':'error', 'message': 'No se proporcionaron datos'}), 400
        
        # Validar campos obligatorios
        campos_requeridos = ['fecha', 'id_mozo', 'id_mesa']
        for campo in campos_requeridos:
            if campo not in data or not data[campo] is None:
                return jsonify({'status':'error', 'message': f'El campo "{campo}" es requerido'}), 400
            
        # Validar tipos de datos
        if not isinstance(data['fecha'], str) or not isinstance(data['id_mozo'], int) or not isinstance(data['id_mesa'], int):
            return jsonify({'status':'error', 'message': 'Tipo de dato inválido para uno o más campos'}), 400
        
        #Validad que el mozo existe y esta activo
        mozo = session.query(Mozo).filter_by(id_mozo=data['id_mozo'], baja=False).first()
        if not mozo:
            return jsonify({'status':'error', 'message': f'No existe un mozo activo con id_mozo {data["id_mozo"]}'}), 400
        
        if mozo.baja:
            return jsonify({'status':'error', 'message': f'El mozo con id_mozo {data["id_mozo"]} está dado de baja'}), 400
        
        #Validad que la mesa existe y esta activa
        mesa = session.query(Mesa).filter_by(id_mesa=data['id_mesa'], baja=False).first()
        if not mesa:
            return jsonify({'status':'error', 'message': f'No existe una mesa activa con id_mesa {data["id_mesa"]}'}), 400
        
        if mesa.baja:
            return jsonify({'status':'error', 'message': f'La mesa con id_mesa {data["id_mesa"]} está dada de baja'}), 400
        
        #Validad duplicados: id_comanda
        if 'id_comanda' in data:
            comanda_existente = session.query(Comanda).filter_by(id_comanda=data['id_comanda']).first()
            if comanda_existente:
                return jsonify({'status':'error', 'message': f'Ya existe una comanda con id_comanda {data["id_comanda"]}'}), 400
            
        # Crear comanda
        nueva_comanda = Comanda(
            fecha=data['fecha'],
            id_mozo=data['id_mozo'],
            id_mesa=data['id_mesa']
        )
        session.add(nueva_comanda)
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
        
        # Actualizar campos permitidos
        if 'fecha' in data:
            comanda.fecha = data['fecha']


        if 'id_mozo' in data:
            nuevo_mozo = session.query(Mozo).filter_by(id_mozo=data['id_mozo']).first()
            if not nuevo_mozo:
                return jsonify({'status':'error', 'message': f'No existe un mozo con id_mozo {data["id_mozo"]}'}), 400
            if nuevo_mozo.baja:
                return jsonify({'status':'error', 'message': f'El mozo con id_mozo {data["id_mozo"]} está dado de baja'}), 400

            comanda.id_mozo = data['id_mozo']



        if 'id_mesa' in data:
            nueva_mesa = session.query(Mesa).filter_by(id_mesa=data['id_mesa']).first()
            if not nueva_mesa:
                return jsonify({'status':'error', 'message': f'No existe una mesa con id_mesa {data["id_mesa"]}'}), 400
        
            if nueva_mesa.baja:
                return jsonify({'status':'error', 'message': f'La mesa con id_mesa {data["id_mesa"]} está dada de baja'}), 400
            
            comanda.id_mesa = data['id_mesa']
        
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
        
        comanda.baja = True
        session.commit()
        return jsonify({
            'status':'success',
            'message': 'Comanda dada de baja exitosamente',
            'data': comanda.json()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error', 'message': f'Error al dar de baja la comanda: {str(e)}'}), 500
    finally:
        session.close()