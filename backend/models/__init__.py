# Importa todos los modelos para mantener compatibilidad con importaciones existentes
from .seccion import Seccion
from .producto import Producto, Plato, Postre, Bebida
from .sector import Sector
from .mesa import Mesa
from .medio_pago import MedioPago
from .mozo import Mozo

# Exporta todos los modelos
__all__ = ['Seccion', 'Producto', 'Plato', 'Postre', 'Bebida', 'Sector', 'Mesa', 'MedioPago', 'Mozo']


