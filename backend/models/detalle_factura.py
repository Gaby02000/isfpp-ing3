from sqlalchemy import Column, Integer, Boolean, ForeignKey, NUMERIC
from sqlalchemy.orm import relationship
from db import Base

class DetalleFactura(Base):
    __tablename__ = 'detalle_factura'
    
    id_detalle_factura = Column(Integer, primary_key=True)
    id_factura = Column(Integer, ForeignKey('factura.id_factura'), nullable=False)
    id_detalle_comanda = Column(Integer, ForeignKey('detalle_comanda.id_detalle_comanda'), nullable=False)
    
    # Relaciones
    detalle_comanda = relationship("DetalleComanda", back_populates="detalle-comanda")
    factura = relationship("Factura", back_populates="factura")
    # detalle_reserva = relationship("DetalleReserva")  # Comentado hasta que exista el modelo DetalleReserva

    
    def json(self):
        return {
            'id_detalle_factura': self.id_detalle_factura,
            'id_factura': self.id_factura,
            'id_detalle_comanda': self.id_detalle_comanda,
        }

