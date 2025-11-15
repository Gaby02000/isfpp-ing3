# Importa todos los modelos para mantener compatibilidad con importaciones existentes
from .seccion import Seccion
from .producto import Producto, Plato, Postre, Bebida
from .sector import Sector
from .mesa import Mesa
from .mozo import Mozo
from .cliente import Cliente

# Exporta todos los modelos
__all__ = ['Seccion', 'Producto', 'Plato', 'Postre', 'Bebida', 'Sector', 'Mesa', 'Mozo', 'Cliente']

