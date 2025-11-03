from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db import Base

class Seccion(Base):
    __tablename__ = 'seccion'
    id_seccion = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False, unique=True)
    baja = Column(Boolean, default=False)
    productos = relationship("Producto", back_populates="seccion")

    def __init__(self, nombre, baja=False):
        self.nombre = nombre
        self.baja = baja

    def json(self):
        return {
            'id_seccion': self.id_seccion,
            'nombre': self.nombre,
            'baja': self.baja,
        }

