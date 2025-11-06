from flask import Blueprint, jsonify, request
from db import SessionLocal
from models import MedioPago

medio_pagos_bp = Blueprint('medio_pagos', __name__)

@medio_pagos_bp.route('/', methods=['GET'])
def listar_medio_pago():
    session = SessionLocal()
    try:
        id_medio_pago = request.args.get('id_medio_pago', type=int)

        # Parámetros de paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        # Validar parámetros de paginación
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        query = session.query(MedioPago)

        if 