from sqlalchemy import Column, Integer, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from db import Base

class DetalleComanda(Base):
    __tablename__ = 'detalle_comanda'
    
    id_detalle_comanda = Column(Integer, primary_key=True)
    id_comanda = Column(Integer, ForeignKey('comanda.id_comanda'), nullable=False)
    id_producto = Column(Integer, ForeignKey('producto.id_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    entregado = Column(Boolean, default=False)
    
    # Relaciones
    comanda = relationship("Comanda", back_populates="detalles")
    producto = relationship("Producto")

    
    def json(self):
        return {
            'id_detalle_comanda': self.id_detalle_comanda,
            'id_comanda': self.id_comanda,
            'id_producto': self.id_producto,
            'producto': self.producto.json() if self.producto else None,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'entregado': self.entregado,
            'subtotal': float(self.precio_unitario * self.cantidad)
        }


