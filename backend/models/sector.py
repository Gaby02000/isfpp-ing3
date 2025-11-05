from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.orm import relationship
from db import Base

class Sector(Base):
    __tablename__ = 'sector'
    
    id_sector = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False, unique=True)
    baja = Column(Boolean, default=False)
    
    # Relaciones
    mesas = relationship("Mesa", back_populates="sector")
    
    def __init__(self, numero, baja=False):
        self.numero = numero
        self.baja = baja

    def json(self):
        return {
            'id_sector': self.id_sector,
            'numero': self.numero,
            'baja': self.baja,
        }

