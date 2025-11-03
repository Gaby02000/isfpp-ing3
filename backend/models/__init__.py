# Importa todos los modelos para mantener compatibilidad con importaciones existentes
from .seccion import Seccion
from .producto import Producto, Plato, Postre, Bebida

# Exporta todos los modelos
__all__ = ['Seccion', 'Producto', 'Plato', 'Postre', 'Bebida']

