from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Mozo(Base):
    __tablename__ = 'mozo'

    id = Column(Integer, primary_key=True)
    documento = Column(String(100), unique=True, nullable=False)
    nombre_apellido = Column(String(255), nullable=False)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(50), nullable=True)
    id_sector = Column(Integer, ForeignKey('sector.id_sector'), nullable=True)
    baja = Column(Boolean, default=False)

    # Relación a Sector
    sector = relationship('Sector', back_populates='mozos')

    def __init__(self, documento, nombre_apellido, id_sector=None, direccion=None, telefono=None, baja=False):
        self.documento = documento
        self.nombre_apellido = nombre_apellido
        self.id_sector = id_sector
        self.direccion = direccion
        self.telefono = telefono
        self.baja = baja

    def json(self):
        return {
            'id': self.id,
            'documento': self.documento,
            'nombre_apellido': self.nombre_apellido,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'id_sector': self.id_sector,
            'baja': self.baja,
        }
