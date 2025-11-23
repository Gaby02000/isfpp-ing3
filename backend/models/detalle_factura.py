from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from db import Base

class DetalleFactura(Base):
    __tablename__ = 'detalle_factura'
    
    id_detalle_factura = Column(Integer, primary_key=True)
    id_factura = Column(Integer, ForeignKey('factura.id_factura'), nullable=False)
    id_detalle_comanda = Column(Integer, ForeignKey('detalle_comanda.id_detalle_comanda'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    
    # Relaciones
    factura = relationship("Factura", back_populates="detalles")
    detalle_comanda = relationship("DetalleComanda", backref="detalle_factura")
    
    def json(self):
        return {
            'id_detalle_factura': self.id_detalle_factura,
            'id_factura': self.id_factura,
            'id_detalle_comanda': self.id_detalle_comanda,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'subtotal': float(self.subtotal),
            'producto': self.detalle_comanda.producto.json() if self.detalle_comanda and self.detalle_comanda.producto else None
        }