from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import Pago, Factura, MedioPago

pago_bp = Blueprint('pago', __name__)

@pago_bp.route('/', methods=['GET'])
def listar_pagos():
    session = SessionLocal()
    try:
        pagos = session.query(Pago).all()
        data = [p.json() for p in pagos]
        return jsonify({'status':'success','data':data}), 200
    except Exception as e:
        return jsonify({'status':'error','message':f'Error al listar pagos: {str(e)}'}), 500
    finally:
        session.close()

@pago_bp.route('/', methods=['POST'])
def crear_pago():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status':'error','message':'No se proporcionaron datos'}), 400

        id_factura = data.get('id_factura')
        id_medio_pago = data.get('id_medio_pago')
        monto = data.get('monto')
        fecha = data.get('fecha')

        # Validaciones básicas
        if not id_factura or not id_medio_pago or monto is None or not fecha:
            return jsonify({'status':'error','message':'Faltan campos requeridos'}), 400

        try:
            id_factura = int(id_factura)
            id_medio_pago = int(id_medio_pago)
            monto = float(monto)
        except (ValueError, TypeError):
            return jsonify({'status':'error','message':'Campos en formato inválido'}), 400

        # Validar existencia de factura y medio de pago
        factura = session.query(Factura).filter_by(id_factura=id_factura).first()
        if not factura:
            return jsonify({'status':'error','message':f'No existe factura con id {id_factura}'}), 400
        medio = session.query(MedioPago).filter_by(id_medio_pago=id_medio_pago).first()
        if not medio:
            return jsonify({'status':'error','message':f'No existe medio de pago con id {id_medio_pago}'}), 400

        pago = Pago(id_factura=id_factura, id_medio_pago=id_medio_pago, monto=monto, fecha=fecha)
        session.add(pago)
        session.commit()
        return jsonify({'status':'success','message':'Pago creado','data':pago.json()}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error','message':f'Error al crear pago: {str(e)}'}), 500
    finally:
        session.close()

@pago_bp.route('/<int:id_pago>', methods=['GET'])
def obtener_pago(id_pago):
    session = SessionLocal()
    try:
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()
        if not pago:
            return jsonify({'status':'error','message':f'No existe pago con id {id_pago}'}), 404
        return jsonify({'status':'success','data':pago.json()}), 200
    except Exception as e:
        return jsonify({'status':'error','message':f'Error al obtener pago: {str(e)}'}), 500
    finally:
        session.close()

@pago_bp.route('/<int:id_pago>', methods=['PUT'])
def modificar_pago(id_pago):
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status':'error','message':'No se proporcionaron datos'}), 400
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()
        if not pago:
            return jsonify({'status':'error','message':f'No existe pago con id {id_pago}'}), 404

        monto = data.get('monto')
        fecha = data.get('fecha')
        if monto is not None:
            try:
                pago.monto = float(monto)
            except (ValueError, TypeError):
                return jsonify({'status':'error','message':'monto inválido'}), 400
        if fecha is not None:
            pago.fecha = fecha

        session.commit()
        return jsonify({'status':'success','message':'Pago actualizado','data':pago.json()}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error','message':f'Error al modificar pago: {str(e)}'}), 500
    finally:
        session.close()

@pago_bp.route('/<int:id_pago>', methods=['DELETE'])
def eliminar_pago(id_pago):
    session = SessionLocal()
    try:
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()
        if not pago:
            return jsonify({'status':'error','message':f'No existe pago con id {id_pago}'}), 404
        session.delete(pago)
        session.commit()
        return jsonify({'status':'success','message':'Pago eliminado'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'status':'error','message':f'Error al eliminar pago: {str(e)}'}), 500
    finally:
        session.close()
