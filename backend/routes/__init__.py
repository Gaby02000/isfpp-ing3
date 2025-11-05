from flask import Blueprint
from .seccion_routes import seccion_bp
from .producto_routes import producto_bp
from .sector_routes import sector_bp
from .mesa_routes import mesa_bp

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(seccion_bp, url_prefix='/secciones')
api_bp.register_blueprint(producto_bp, url_prefix='/productos')
api_bp.register_blueprint(sector_bp, url_prefix='/sectores')
api_bp.register_blueprint(mesa_bp, url_prefix='/mesas')