from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Factura(Base):
    __tablename__ = 'cliente'
    
    id_factura = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True)
    fecha = Column(String(50), nullable=False)
    total = Column(Numeric(10,2), nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    id_comanda = Column(Integer, ForeignKey('comanda.id_comanda'), nullable=True)

    
    # Relaciones
    cliente = relationship("Cliente", back_populates="cliente")
    comanda = relationship("Comanda", back_populates="comanda")
    
    def __init__(self, codigo, fecha, total, id_cliente, id_comanda):
        self.codigo = codigo
        self.fecha = fecha
        self.total = total
        self.id_cliente = id_cliente
        self.id_comanda = id_comanda


    def json(self):
        return {
            'id_factura': self.id_factura,
            'codigo': self.codigo,
            'fecha': self.fecha,
            'total': self.total,
            'id_cliente': self.id_cliente,
            'id_comanda': self.id_comanda,
        }