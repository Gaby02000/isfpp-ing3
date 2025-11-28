from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from db import Base


class Pago(Base):
    __tablename__ = 'pago'
    
    id_pago = Column(Integer, primary_key=True)
    id_factura = Column(Integer, ForeignKey('factura.id_factura'), nullable=False)
    id_medio_pago = Column(Integer, ForeignKey('medio_pago.id_medio_pago'), nullable=False)
    monto = Column(Numeric(10,2), nullable=False)
    fecha = Column(String(50), nullable=False)

    
    # Relaciones
    factura = relationship("Factura", back_populates="pagos")
    medio_pago = relationship("MedioPago", back_populates="pagos")

    def __init__(self, id_factura, id_medio_pago, monto, fecha):
        self.id_factura = id_factura
        self.id_medio_pago = id_medio_pago      
        self.monto = monto
        self.fecha = fecha

    def json(self):
        return {
            'id_pago': self.id_pago,
            'id_factura': self.id_factura,
            'factura_codigo': self.factura.codigo if self.factura else None,
            'id_medio_pago': self.id_medio_pago,
            'medio_pago_nombre': self.medio_pago.nombre if self.medio_pago else None,
            'monto': float(self.monto),
            'fecha': self.fecha,
        }

