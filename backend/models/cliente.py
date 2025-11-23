from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db import Base

class Cliente(Base):
    __tablename__ = 'cliente'
    
    id_cliente = Column(Integer, primary_key=True)
    documento = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    num_telefono = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    baja = Column(Boolean, default=False)
    
    # Relaciones
    #comandas = relationship("Comanda", back_populates="cliente")
    factura = relationship("Factura", back_populates="cliente")

    
    def __init__(self, documento, nombre, apellido, num_telefono, email, baja=False):
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.num_telefono = num_telefono
        self.email = email
        self.baja = baja

    def json(self):
        return {
            'id_cliente': self.id_cliente,
            'documento': self.documento,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'num_telefono': self.num_telefono,
            'email': self.email,
            'baja': self.baja
        }