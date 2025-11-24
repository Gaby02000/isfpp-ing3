from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class MedioPago(Base):
    __tablename__ = 'medio_pago'
    
    id_medio_pago = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)
    baja = Column(Boolean, default=False)
    
    # Relaciones
    pagos = relationship("Pago", back_populates="medio_pago")
    
    def __init__(self, nombre, descripcion=None, baja=False):
        self.nombre = nombre
        self.descripcion = descripcion
        self.baja = baja

    def json(self):
        return {
            'id_medio_pago': self.id_medio_pago,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'baja': self.baja,
        }