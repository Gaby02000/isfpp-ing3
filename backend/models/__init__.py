# Importa todos los modelos para mantener compatibilidad con importaciones existentes
from .seccion import Seccion
from .producto import Producto, Plato, Postre, Bebida
from .sector import Sector
from .mesa import Mesa
from .medio_pago import MedioPago
from .mozo import Mozo
from .cliente import Cliente
from .comanda import Comanda
from .detalle_comanda import DetalleComanda
from .factura import Factura
from .detalle_factura import DetalleFactura

# Exporta todos los modelos
__all__ = ['Seccion', 'Producto', 'Plato', 'Postre', 'Bebida', 'Sector', 'Mesa', 'MedioPago', 'Mozo', 'Cliente', 'Comanda', 'DetalleComanda', 'Factura', 'DetalleFactura']


