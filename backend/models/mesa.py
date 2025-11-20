from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Mesa(Base):
    __tablename__ = 'mesa'
    
    id_mesa = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False, unique=True)
    tipo = Column(String(50), nullable=False)
    cant_comensales = Column(Integer, nullable=False)
    id_sector = Column(Integer, ForeignKey('sector.id_sector'), nullable=False)
    baja = Column(Boolean, default=False)
    
    # Relaciones
    sector = relationship("Sector", back_populates="mesas")
    comandas = relationship("Comanda", back_populates="mesa")
    
    def __init__(self, numero, tipo, cant_comensales, id_sector, baja=False):
        self.numero = numero
        self.tipo = tipo
        self.cant_comensales = cant_comensales
        self.id_sector = id_sector
        self.baja = baja

    def json(self):
        return {
            'id_mesa': self.id_mesa,
            'numero': self.numero,
            'tipo': self.tipo,
            'cant_comensales': self.cant_comensales,
            'id_sector': self.id_sector,
            'sector': self.sector.json() if self.sector else None,
            'baja': self.baja,
        }

