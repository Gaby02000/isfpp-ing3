from flask import Blueprint
from .seccion_routes import seccion_bp
from .producto_routes import producto_bp

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(seccion_bp, url_prefix='/secciones')
api_bp.register_blueprint(producto_bp,url_prefix='/productos')